#!/usr/bin/env python3
"""Axion audit v2: per-engagement file inventory with Drive coverage check.

Uses subprocess `find` (with timeout) to enumerate Drive filenames per engagement,
so cloud-only file stat-storms can't hang Python's os.walk.
"""
import os
import sys
import subprocess
import json
from pathlib import Path

DRIVE = Path("/Users/iris/Library/CloudStorage/GoogleDrive-ivo@iris.ai/.shortcut-targets-by-id/0B1Dd1wWV_2fRLXFaV2ppdTBqMzA/Iris.ai - Everyone")
AXION = Path("/Users/iris/Documents/Axion/scoping")
OUT = Path("/Users/iris/Documents/atlas/_axion_audit")

# Drive locations to scan per engagement
DRIVE_LOCATIONS = {
    "postbank": ["Commercial/Account Management /Postbank"],
    "aumovio": [
        "Commercial/Account Management /Continental Aumovio",
        "Commercial/POC/Scoping Exercises/Aumovio",
    ],
    "heineken": [
        "Commercial/Account Management /Heineken",
        "Commercial/POC/Scoping Exercises/Heineken",
        "Commercial/POC/POC Data/Heineken Procurement 03.25",
    ],
    "welocalize": [
        "Commercial/Account Management /WeLocalize",
        "Commercial/POC/Scoping Exercises/Welocalize",
    ],
    "garrett": ["Commercial/Account Management /Garrett"],
    "sms-group": ["Commercial/Account Management /SMS Group"],
    "tandf": ["Commercial/POC/Scoping Exercises/TandF"],
    "agrolimen": ["Commercial/Account Management /Agrolimen"],
    "fresenius": ["Commercial/Account Management /Fresenius"],
    "deutschebahn": ["Commercial/POC/Scoping Exercises/DeutscheBahn"],
    "nhs": ["Commercial/Account Management /Client specific material (Cleaning In Progress) /NHS - Rabih Wassel"],
    "alexfert": [
        "Commercial/Account Management /Alexfert",
        "Commercial/Playground & Demo/Axion Demo Datasets/AlexFert",
        "Commercial/Playground & Demo/Axion Demo Datasets/AlexFert Demo",
        "Commercial/Playground & Demo/Axion Demo Datasets/AlexFert Demo 2",
    ],
    "shanghai-synocodes": ["Commercial/Account Management /Shanghai Synocodes "],
    "stepan": [
        "Commercial/Account Management /Stepan Company",
        "Commercial/POC/Scoping Exercises/Stepan Company",
    ],
    "cetin": ["Commercial/Account Management /CETIN"],
    "yettel": ["Commercial/Account Management /Yettel"],
    "hubspot": [],  # no client; internal exploration
    "aumovio-soft-impact": ["Commercial/Account Management /Continental Aumovio"],
}

CODE_EXT = {".py", ".ipynb", ".sh", ".yaml", ".yml", ".toml", ".cfg", ".ini",
            ".dockerfile", ".js", ".ts", ".jsx", ".tsx", ".tf", ".env",
            ".bash", ".zsh"}
CODE_NAMES = {"requirements.txt", "Dockerfile", ".env.example", "Makefile",
              "pyproject.toml", "package.json", "setup.py", ".gitignore"}
DATA_EXT = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
            ".dwg", ".dxf", ".tsv", ".zip", ".tar", ".gz", ".7z",
            ".rar", ".eml", ".msg"}
# CSV is ambiguous: client data sample vs extraction output. We disambiguate
# in categorise() based on path/name.
OUTPUT_HINTS = {"extracted_", "extraction_results", "_results", "_extracted",
                "showcase.html", "deliverable"}


def human_size(n):
    n = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def categorise(path: Path) -> str:
    name = path.name
    nl = name.lower()
    ext = path.suffix.lower()

    if name in (".DS_Store", ".gitkeep", "Thumbs.db") or name.startswith("~$"):
        return "other"
    if name in CODE_NAMES or ext in CODE_EXT:
        return "code"

    parent = path.parent.name.lower()
    if any(h in nl for h in OUTPUT_HINTS):
        return "output"
    if parent in ("results", "results-llm", "extracted", "outputs", "output",
                  "deliverables", "extraction_results"):
        return "output"
    if "showcase" in nl and ext == ".html":
        return "output"
    # Common extraction-output patterns in xlsx/json filenames
    if "_output" in nl or "_ontology_output" in nl:
        return "output"
    if "extraction-week" in str(path).lower() or "extraction_week" in str(path).lower():
        # Files inside a weekly-extraction subfolder are likely outputs
        return "output"
    # IRIS-authored exhibits (verification matrices, comparison sheets)
    if any(t in nl for t in ("v5_vs", "v6_vs", "v7_vs", "_three_way", "three_way",
                              "_comparison_", "_verification")):
        return "output"

    if ext == ".json":
        if "prompt" in nl or "schema" in nl or "config" in nl:
            return "code"
        return "output"
    if ext in (".jsonl", ".ndjson"):
        return "output"

    if ext in (".md", ".txt", ".rst"):
        return "other"

    # CSV: output if extraction-style filename (_page_NN, extracted_, _table_, etc),
    # else treat as client data.
    if ext == ".csv":
        if any(t in nl for t in ("_page_", "_table_", "extracted_", "_extracted",
                                  "_v2", "_v3", "_v4", "_chunk", "_results",
                                  "_translated")):
            return "output"
        # CSVs alongside output HTML at the same stem path = output
        sibling_html = path.with_suffix(".html")
        if sibling_html.exists():
            return "output"
        return "data"

    # showcase / deliverable PDFs are outputs not client data
    if "showcase" in nl or "deliverable" in nl:
        return "output"

    if ext in DATA_EXT:
        return "data"
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".heic", ".bmp"):
        return "other"
    if ext == ".html":
        return "output"
    if ext == ".har":
        return "other"
    if ext in (".otf", ".ttf", ".woff", ".woff2"):
        return "other"
    return "other"


def build_drive_index(co: str, timeout_s: int = 90) -> dict:
    """Use `find` via subprocess (with timeout) to list filenames.

    Returns dict: lowercased_name -> [relative_drive_path, ...]
    """
    idx = {}
    for subpath in DRIVE_LOCATIONS.get(co, []):
        root = DRIVE / subpath
        if not root.exists():
            print(f"  ! drive path missing: {root}", file=sys.stderr)
            continue
        try:
            # Use find with timeout. Print just filenames + relative paths.
            r = subprocess.run(
                ["find", str(root), "-type", "f"],
                capture_output=True, text=True, timeout=timeout_s,
            )
            for line in r.stdout.splitlines():
                p = line.strip()
                if not p:
                    continue
                name = os.path.basename(p)
                if name.startswith(".") or name.startswith("~$"):
                    continue
                idx.setdefault(name.lower(), []).append(p)
        except subprocess.TimeoutExpired:
            print(f"  ! TIMEOUT scanning {root} after {timeout_s}s", file=sys.stderr)
        except Exception as e:
            print(f"  ! drive scan error {root}: {e}", file=sys.stderr)
    return idx


def check_drive(name: str, drive_idx: dict) -> str:
    key = name.lower()
    if key in drive_idx:
        matches = drive_idx[key]
        short = matches[0].split("Iris.ai - Everyone/")[-1]
        if len(matches) > 1:
            return f"yes ({len(matches)}x, {short[:80]})"
        return f"yes ({short[:100]})"
    stem = Path(name).stem.lower()
    if stem:
        for k, v in drive_idx.items():
            if Path(k).stem == stem:
                return f"yes-stem ({v[0].split('Iris.ai - Everyone/')[-1][:80]})"
    return "no"


def audit_engagement(co: str, group_subfolders: bool = False):
    src = AXION / co
    if not src.exists() or not any(src.iterdir()):
        return None

    print(f"== Auditing {co} ==", file=sys.stderr)
    drive_idx = build_drive_index(co)
    print(f"   drive idx: {len(drive_idx)} unique filenames", file=sys.stderr)

    rows = []
    cat_counts = {"data": 0, "code": 0, "output": 0, "other": 0}
    cat_sizes = {"data": 0, "code": 0, "output": 0, "other": 0}
    orphans = []
    drive_matches = 0
    total_size = 0
    total_files = 0
    subfolder_stats = {}

    EXCLUDE_DIRS = {"__pycache__", ".venv", "venv", ".env", "node_modules",
                    ".git", ".idea", ".vscode", ".mypy_cache", ".pytest_cache",
                    "dist", "build", ".ipynb_checkpoints", "site-packages",
                    ".ruff_cache", ".tox"}
    excluded_files = 0
    excluded_size = 0
    for dp, dirs, files in os.walk(src):
        # Drop excluded dirs IN-PLACE so os.walk skips them
        kept = []
        for d in dirs:
            if d in EXCLUDE_DIRS:
                # Tally what we're skipping for reporting
                try:
                    for edp, _, efs in os.walk(os.path.join(dp, d)):
                        for ef in efs:
                            try:
                                excluded_size += os.path.getsize(os.path.join(edp, ef))
                                excluded_files += 1
                            except OSError:
                                pass
                except Exception:
                    pass
                continue
            kept.append(d)
        dirs[:] = kept
        rel_dir = os.path.relpath(dp, src)
        top = "<root>" if rel_dir == "." else rel_dir.split(os.sep)[0]
        for f in files:
            p = Path(dp) / f
            try:
                sz = p.stat().st_size
            except OSError:
                sz = 0
            total_files += 1
            total_size += sz
            cat = categorise(p)
            cat_counts[cat] += 1
            cat_sizes[cat] += sz
            in_drive = check_drive(f, drive_idx)
            if cat == "data" and in_drive == "no":
                orphans.append(str(p.relative_to(src)))
            if in_drive.startswith("yes"):
                drive_matches += 1

            rows.append((str(p.relative_to(src)), sz, cat, in_drive))

            s = subfolder_stats.setdefault(top, {
                "n": 0, "size": 0,
                "data": 0, "code": 0, "output": 0, "other": 0,
                "drive": 0, "orphan_data": 0, "code_files": []
            })
            s["n"] += 1
            s["size"] += sz
            s[cat] += 1
            if in_drive.startswith("yes"):
                s["drive"] += 1
            if cat == "data" and in_drive == "no":
                s["orphan_data"] += 1
            if cat == "code":
                s["code_files"].append((str(p.relative_to(src)), sz, in_drive))

    return {
        "co": co,
        "total_size": total_size,
        "total_files": total_files,
        "cat_counts": cat_counts,
        "cat_sizes": cat_sizes,
        "drive_matches": drive_matches,
        "orphans": orphans,
        "rows": rows,
        "subfolder_stats": subfolder_stats,
        "grouped": group_subfolders,
        "excluded_files": excluded_files,
        "excluded_size": excluded_size,
    }


def render_md(result):
    co = result["co"]
    n = result["total_files"]
    sz = result["total_size"]
    cc = result["cat_counts"]
    cs = result["cat_sizes"]
    coverage = (result["drive_matches"] / n * 100) if n else 0

    L = []
    L.append(f"# Axion audit: {co}\n")
    L.append("## Summary")
    L.append(f"- Total size: {human_size(sz)}")
    L.append(f"- File count: {n}")
    L.append(f"- Categories breakdown: data {cc['data']} / code {cc['code']} / output {cc['output']} / other {cc['other']}")
    L.append(f"- Category sizes: data {human_size(cs['data'])} / code {human_size(cs['code'])} / output {human_size(cs['output'])} / other {human_size(cs['other'])}")
    L.append(f"- Drive coverage: {coverage:.1f}% of files have a Drive equivalent by filename")
    L.append(f"- Orphan count (data files NOT in Drive): {len(result['orphans'])}")
    if result.get("excluded_files"):
        L.append(f"- Excluded from audit (.venv/node_modules/.git/etc): {result['excluded_files']} files, {human_size(result['excluded_size'])}")
    L.append("")

    if result.get("grouped"):
        L.append("## Files (grouped by subfolder; >500MB engagement)\n")
        L.append("| Subfolder | Files | Size | data | code | output | other | Drive cov | Orphan data |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for sub, s in sorted(result["subfolder_stats"].items(), key=lambda x: -x[1]["size"]):
            cov = (s["drive"] / s["n"] * 100) if s["n"] else 0
            L.append(f"| `{sub}` | {s['n']} | {human_size(s['size'])} | {s['data']} | {s['code']} | {s['output']} | {s['other']} | {cov:.0f}% | {s['orphan_data']} |")
        L.append("")
        L.append("## Drill: code files\n")
        any_code = False
        for sub, s in sorted(result["subfolder_stats"].items()):
            if not s["code_files"]:
                continue
            any_code = True
            L.append(f"### `{sub}/`\n")
            L.append("| Path | Size | In Drive? |")
            L.append("|---|---|---|")
            for path, fsz, drv in sorted(s["code_files"]):
                L.append(f"| {path} | {human_size(fsz)} | {drv} |")
            L.append("")
        if not any_code:
            L.append("(no code files found)\n")
    else:
        L.append("## Files\n")
        L.append("| Path | Size | Category | In Drive? |")
        L.append("|---|---|---|---|")
        for path, fsz, cat, drv in sorted(result["rows"]):
            L.append(f"| {path} | {human_size(fsz)} | {cat} | {drv} |")
        L.append("")

    L.append("## Findings\n")
    if result["orphans"]:
        L.append(f"- {len(result['orphans'])} data file(s) NOT in Drive (orphans, need upload-before-delete):")
        for o in result["orphans"][:25]:
            L.append(f"  - `{o}`")
        if len(result["orphans"]) > 25:
            L.append(f"  - ... (+{len(result['orphans']) - 25} more)")
    else:
        L.append("- No data orphans: every client-document filename has a Drive match.")
    L.append("")
    L.append(f"- Code files to move into engagements/{co}/<stage>/: {cc['code']} files ({human_size(cs['code'])})")
    L.append(f"- Output files to move to Drive iris-outputs/ or S3: {cc['output']} files ({human_size(cs['output'])})")
    L.append("")
    L.append("## Migration recommendation\n")
    L.append(f"- Delete-after-Drive-verified: {cc['data'] + cc['other']} files, {human_size(cs['data'] + cs['other'])} (data already in Drive + noise/notes/images)")
    L.append(f"- Move to repo: {cc['code']} files, {human_size(cs['code'])}")
    L.append(f"- Upload to Drive first (orphans): {len(result['orphans'])} files")
    return "\n".join(L) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    LARGE = {"sms-group", "tandf", "garrett", "alexfert"}

    only = sys.argv[1:] if len(sys.argv) > 1 else list(DRIVE_LOCATIONS.keys())
    results = {}
    for co in only:
        if not (AXION / co).exists():
            print(f"-- skip {co} (no Axion folder)", file=sys.stderr)
            continue
        r = audit_engagement(co, group_subfolders=(co in LARGE))
        if r:
            results[co] = r
            (OUT / f"{co}.md").write_text(render_md(r))
            print(f"  wrote {co}.md ({r['total_files']} files, {human_size(r['total_size'])})", file=sys.stderr)

    # Save aggregate raw (merge with existing if any)
    raw_path = OUT / "_raw.json"
    existing = {}
    if raw_path.exists():
        try:
            existing = json.loads(raw_path.read_text())
        except Exception:
            existing = {}
    for co, r in results.items():
        existing[co] = {
            "total_size": r["total_size"],
            "total_files": r["total_files"],
            "cat_counts": r["cat_counts"],
            "cat_sizes": r["cat_sizes"],
            "drive_matches": r["drive_matches"],
            "orphan_count": len(r["orphans"]),
            "excluded_files": r.get("excluded_files", 0),
            "excluded_size": r.get("excluded_size", 0),
        }
    raw_path.write_text(json.dumps(existing, indent=2))
    print("Done.", file=sys.stderr)


if __name__ == "__main__":
    main()
