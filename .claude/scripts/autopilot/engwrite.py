"""Safe writes into the engagements repo for the meeting autopilot.

Rules this module enforces:
  - only the files the autopilot names are committed; nothing else is staged
    (never `git add -A`; other people's uncommitted work is left exactly as it was)
  - the commit is built from HEAD's version of each file plus the autopilot's
    change, so uncommitted edits Ivo has in the same file stay uncommitted
  - aborts (raises WriteRefused) when the branch is not master, a merge/rebase
    is in progress, or a target file has staged changes
  - every autopilot block is wrapped in markers so it can be replaced or undone:
        <!-- autopilot:<key> -->
        ...entry...
        <!-- /autopilot:<key> -->

Plumbing: temp index (GIT_INDEX_FILE) -> read-tree HEAD -> update-index with new
blobs -> write-tree -> commit-tree -> update-ref (with old-value check), then
the real index entry and the working file are updated for the same paths only.
"""
import fcntl
import os
import re
import subprocess
import tempfile
import time
from contextlib import contextmanager

BRANCH = "master"


class WriteRefused(Exception):
    pass


def _git(repo, *args, input=None, env=None, check=True):
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(["git", "-C", repo, *args], input=input, capture_output=True,
                       text=True, env=e)
    if check and r.returncode != 0:
        raise WriteRefused(f"git {' '.join(args[:2])} failed: {r.stderr.strip()[:300]}")
    return r.stdout


@contextmanager
def repo_lock(lock_path):
    os.makedirs(os.path.dirname(lock_path), exist_ok=True)
    with open(lock_path, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _preflight(repo, branch):
    gd = _git(repo, "rev-parse", "--absolute-git-dir").strip()
    cur = _git(repo, "symbolic-ref", "--short", "-q", "HEAD", check=False).strip()
    if cur != branch:
        raise WriteRefused(f"engagements repo is on '{cur or 'detached'}', not {branch}")
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        if os.path.exists(os.path.join(gd, marker)):
            raise WriteRefused(f"git operation in progress ({marker})")
    for _ in range(20):
        if not os.path.exists(os.path.join(gd, "index.lock")):
            return gd
        time.sleep(0.5)
    raise WriteRefused("index.lock held for 10s")


def _blob_at(repo, rev, path):
    out = _git(repo, "rev-parse", "-q", "--verify", f"{rev}:{path}", check=False).strip()
    return out or None


def _index_blob(repo, path):
    out = _git(repo, "ls-files", "-s", "--", path).strip()
    return out.split()[1] if out else None


def commit_paths(repo, changes, message, lock_path, branch=BRANCH):
    """changes: {relpath: transform}; transform(text_or_None) -> new_text or None (= delete).

    Returns the new commit sha. Raises WriteRefused without touching anything on refusal.
    """
    with repo_lock(lock_path):
        _preflight(repo, branch)
        head = _git(repo, "rev-parse", "HEAD").strip()
        plan = []
        for path, fn in changes.items():
            hb = _blob_at(repo, "HEAD", path)
            ib = _index_blob(repo, path)
            if hb != ib:
                raise WriteRefused(f"{path} has staged changes; not touching it")
            head_text = _git(repo, "cat-file", "blob", hb) if hb else None
            wp = os.path.join(repo, path)
            work_text = open(wp, encoding="utf-8").read() if os.path.exists(wp) else None
            new_head = fn(head_text)
            if work_text == head_text:
                new_work = new_head
            else:
                try:
                    new_work = fn(work_text)
                except Exception:
                    raise WriteRefused(f"{path}: working copy differs and the change does not apply to it")
            if new_head == head_text:
                continue
            plan.append((path, new_head, new_work))
        if not plan:
            return None
        blobs = {}
        fd, tmp_index = tempfile.mkstemp(prefix="ap_index_")
        os.close(fd)
        try:
            env = {"GIT_INDEX_FILE": tmp_index}
            _git(repo, "read-tree", "HEAD", env=env)
            for path, new_head, _ in plan:
                if new_head is None:
                    _git(repo, "update-index", "--force-remove", "--", path, env=env)
                else:
                    b = _git(repo, "hash-object", "-w", "--stdin", input=new_head).strip()
                    blobs[path] = b
                    _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{b},{path}", env=env)
            tree = _git(repo, "write-tree", env=env).strip()
        finally:
            os.unlink(tmp_index)
        commit = _git(repo, "commit-tree", tree, "-p", head, "-m", message).strip()
        _git(repo, "update-ref", f"refs/heads/{branch}", commit, head)
        for path, new_head, new_work in plan:
            if new_head is None:
                _git(repo, "update-index", "--force-remove", "--", path)
            else:
                _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blobs[path]},{path}")
            wp = os.path.join(repo, path)
            if new_work is None:
                if os.path.exists(wp):
                    os.unlink(wp)
            else:
                os.makedirs(os.path.dirname(wp), exist_ok=True)
                with open(wp, "w", encoding="utf-8") as f:
                    f.write(new_work)
        return commit


# ---------------------------------------------------------------- block transforms
def _start(key):
    return f"<!-- autopilot:{key} -->"


def _end(key):
    return f"<!-- /autopilot:{key} -->"


def block(key, body):
    return f"{_start(key)}\n{body.strip()}\n{_end(key)}\n"


def has_block(text, key):
    return bool(text) and _start(key) in text


def _block_rx(key):
    return re.compile(re.escape(_start(key)) + r".*?" + re.escape(_end(key)) + r"\n?\n?", re.S)


def upsert_status(key, body):
    """Insert the entry newest-on-top (before the first '## ' header) or replace an existing block."""
    def fn(text):
        text = text or ""
        blk = block(key, body)
        if has_block(text, key):
            return _block_rx(key).sub(lambda _: blk + "\n", text, count=1)
        m = re.search(r"^(<!-- autopilot:[^\n]*-->\n)?## ", text, re.M)
        if m:
            return text[:m.start()] + blk + "\n" + text[m.start():]
        return text.rstrip("\n") + "\n\n" + blk
    return fn


def upsert_under_heading(key, body, heading_patterns, fallback_heading):
    """Insert a block right after the first matching '## ' heading (and its blank line); else append a section."""
    def fn(text):
        text = text or ""
        blk = block(key, body)
        if has_block(text, key):
            return _block_rx(key).sub(lambda _: blk + "\n", text, count=1)
        for pat in heading_patterns:
            m = re.search(rf"^## [^\n]*{pat}[^\n]*\n(\n)?", text, re.M | re.I)
            if m:
                return text[:m.end()] + blk + "\n" + text[m.end():]
        return text.rstrip("\n") + f"\n\n## {fallback_heading}\n\n" + blk
    return fn


def remove_block(key):
    def fn(text):
        if text is None or not has_block(text, key):
            return text
        return _block_rx(key).sub("", text, count=1)
    return fn


def create_file(content):
    def fn(text):
        return content if text is None else text   # never overwrite a file that exists
    return fn


def replace_if_same(old, new):
    """Overwrite a file the autopilot wrote, only while it still holds exactly what we wrote."""
    def fn(text):
        return new if text == old else text
    return fn


def delete_if_same(old):
    def fn(text):
        return None if text == old else text
    return fn
