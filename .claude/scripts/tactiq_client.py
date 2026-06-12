#!/usr/bin/env python3
"""Tactiq GraphQL client. Provides auth + meeting fetch.

Credentials come from ~/.tactiq-credentials.json (NOT committed). Format:
{
  "api_key": "...",
  "refresh_token": "...",
  "id_token": "..."
}

The id_token is rotated automatically when it expires. The refresh_token is long-lived;
get a fresh one by signing into app.tactiq.io and inspecting the request payload of a
graphql call (the bearer token + the refreshToken in firebase localStorage).
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

CREDS_PATH = os.path.expanduser("~/.tactiq-credentials.json")
GQL = "https://api2.tactiq.io/api/2/graphql"

LIST_QUERY = "query ListMeetings($type: MeetingType!, $offset: Int, $filter: SearchFilterInput!, $sortBy: SortBy) { meetings(type: $type, offset: $offset, filter: $filter, sortBy: $sortBy) { offset hasMore meetings { id title created } } }"

MEETING_QUERY = "query meetingWithTranscript($meetingId: ID!) { meeting(id: $meetingId) { id title created participants { name } duration languageCode transcript } }"

PAGE_SIZE = 50


def _load_creds():
    if not os.path.exists(CREDS_PATH):
        raise SystemExit(
            f"ERROR: tactiq credentials not found at {CREDS_PATH}\n"
            f"Create the file with:\n"
            f'  {{"api_key": "...", "refresh_token": "...", "id_token": "..."}}\n'
            f"Get the refresh_token by signing into app.tactiq.io and inspecting "
            f"firebase localStorage, plus a recent graphql request payload for id_token."
        )
    with open(CREDS_PATH) as f:
        return json.load(f)


def _save_creds(creds):
    with open(CREDS_PATH, "w") as f:
        json.dump(creds, f, indent=2)


_CREDS = _load_creds()


def refresh_id_token():
    req = urllib.request.Request(
        f"https://securetoken.googleapis.com/v1/token?key={_CREDS['api_key']}",
        data=f"grant_type=refresh_token&refresh_token={_CREDS['refresh_token']}".encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    _CREDS["id_token"] = data["id_token"]
    _save_creds(_CREDS)
    print(f"  [refreshed token, expires in {data.get('expires_in')}s]", file=sys.stderr)


def gql(op_name, query, variables, retries=3):
    body = json.dumps({"operationName": op_name, "query": query, "variables": variables}).encode()
    refreshed = False
    for attempt in range(retries):
        req = urllib.request.Request(
            GQL,
            data=body,
            headers={
                "authorization": f"Bearer {_CREDS['id_token']}",
                "content-type": "application/json",
                "origin": "https://app.tactiq.io",
                "referer": "https://app.tactiq.io/",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
                "accept": "*/*",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            # Tactiq returns both 401/403 AND 500 for expired tokens. Refresh once on
            # any of these, then fall through to backoff for legitimate 500s.
            if e.code in (401, 403, 500) and not refreshed:
                print(f"  auth-like error {e.code}, refreshing token...", file=sys.stderr)
                refresh_id_token()
                refreshed = True
                continue
            if e.code >= 500 and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError(f"failed after {retries} attempts")


def slug(s, maxlen=80):
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE).strip()
    s = re.sub(r"\s+", "_", s)
    return s[:maxlen] or "untitled"


def fmt_ts(ms_epoch, origin_ms):
    delta = max(0, (ms_epoch - origin_ms) // 1000)
    h, rem = divmod(delta, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def format_transcript(meeting):
    """Return (header_dict, body_text) or None if no transcript."""
    t = meeting.get("transcript")
    if not t or not t.get("blocks"):
        return None
    blocks = [b for b in t["blocks"] if not b.get("isDeleted") and b.get("transcript", "").strip()]
    if not blocks:
        return None
    origin = min(b["timestamp"] for b in blocks)
    lines = []
    for b in blocks:
        ts = fmt_ts(b["timestamp"], origin)
        speaker = b.get("speakerName") or "Unknown"
        text = b["transcript"].strip()
        lines.append(f"[{ts}] {speaker}: {text}")

    created_ms = meeting.get("created")
    date = datetime.fromtimestamp(created_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d") if created_ms else "unknown"
    header = {
        "title": meeting.get("title") or "untitled",
        "date": date,
        "meeting_id": meeting["id"],
        "duration_s": meeting.get("duration") or 0,
        "participants": [p["name"] for p in (meeting.get("participants") or [])],
        "language": meeting.get("languageCode", ""),
    }
    return header, "\n".join(lines)


def fetch_meeting(meeting_id):
    """Fetch one meeting. Returns (header, body) or raises."""
    r = gql("meetingWithTranscript", MEETING_QUERY, {"meetingId": meeting_id})
    m = r["data"]["meeting"]
    if not m:
        raise SystemExit(f"meeting not found: {meeting_id}")
    result = format_transcript(m)
    if result is None:
        raise SystemExit(f"meeting has no transcript: {meeting_id}")
    return result


def list_meetings():
    """List all meetings (paginated). Returns list of dicts."""
    all_meetings = []
    offset = 0
    while True:
        r = gql("ListMeetings", LIST_QUERY, {
            "type": "MyMeetings",
            "offset": offset,
            "filter": {},
            "sortBy": "CREATED_NEWEST_FIRST",
        })
        page = r["data"]["meetings"]
        all_meetings.extend(page["meetings"])
        if not page["hasMore"]:
            break
        offset += PAGE_SIZE
    return all_meetings


def render_with_header(header, body):
    """Render a full transcript file with metadata header."""
    return (
        f"Title: {header['title']}\n"
        f"Date: {header['date']}\n"
        f"Meeting ID: {header['meeting_id']}\n"
        f"Duration: {header['duration_s']}s\n"
        f"Participants: {', '.join(header['participants'])}\n"
        f"Language: {header['language']}\n"
        f"{'=' * 60}\n\n"
        f"{body}\n"
    )


def extract_meeting_id(arg):
    """Accept either a raw meeting ID or a Tactiq URL."""
    # URLs look like https://app.tactiq.io/meeting/<id> or /transcripts/<id>
    m = re.search(r"(?:meeting|transcripts)/([A-Za-z0-9]+)", arg)
    if m:
        return m.group(1)
    return arg.strip()
