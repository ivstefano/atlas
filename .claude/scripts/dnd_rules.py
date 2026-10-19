#!/usr/bin/env python3
"""Decide whether a calendar event is a client meeting worth silencing Slack for.

Rule, in order (first match wins):
  1. Not a DEFAULT event (out-of-office, focus time, birthday) -> not client
  2. Title contains an internal marker -> not client
  3. Every external attendee domain is deny-listed -> not client
  4. At least one external attendee remains -> CLIENT
  5. Otherwise (all-internal or solo) -> not client

Calibrated against 85 real events, 2026-08-25..2026-09-07. Ivo's decisions:
  - external attendees only; client name in the title is NOT enough
  - partners/vendors are deny-listed, they are not clients
"""

HOME_DOMAIN = "iris.ai"

# External domains that are never a client: personal accounts used by team /
# contractors, plus partners and vendors.
DENY_DOMAINS = {
    "gmail.com",          # team + contractor personal accounts
    "growth-mojo.com",    # partner
    "marketstar.com",     # partner
    "dezea.digital",      # web agency (vendor)
}

INTERNAL_TITLE_MARKERS = ("[internal]",)

# Shared calendars get invited as attendees; they are not people.
IGNORE_DOMAIN_SUFFIXES = ("group.calendar.google.com",)


def domains_of(attendees):
    out = set()
    for a in attendees or []:
        email = (a.get("email") or "").strip().lower()
        if "@" not in email:
            continue
        dom = email.rsplit("@", 1)[1]
        if dom.endswith(IGNORE_DOMAIN_SUFFIXES):
            continue
        out.add(dom)
    return out


def classify(event):
    """Return (is_client: bool, reason: str)."""
    # Calendar API returns lowercase ("default"), the MCP layer uppercase
    # ("DEFAULT"); normalise so both sources classify identically.
    etype = (event.get("eventType") or "default").lower()
    if etype != "default":
        return False, f"eventType={etype}"

    title = (event.get("summary") or "").lower()
    for marker in INTERNAL_TITLE_MARKERS:
        if marker in title:
            return False, f"title marker {marker!r}"

    doms = domains_of(event.get("attendees"))
    if not doms:
        return False, "no attendees"

    external = {d for d in doms if d != HOME_DOMAIN}
    if not external:
        return False, "all internal"

    allowed = external - DENY_DOMAINS
    if not allowed:
        return False, "external all deny-listed: " + ",".join(sorted(external))

    return True, "client domain: " + ",".join(sorted(allowed))


def is_meeting(event):
    """Any real call on the calendar (client or internal), for the meeting-state
    cache read by notify_hook.py. Timed DEFAULT event, at least one other
    attendee, not declined by Ivo."""
    if (event.get("eventType") or "default").lower() != "default":
        return False
    if not (event.get("start") or {}).get("dateTime"):
        return False  # all-day
    others = 0
    for a in event.get("attendees") or []:
        if a.get("self"):
            if a.get("responseStatus") == "declined":
                return False
            continue
        if (a.get("email") or "").endswith("group.calendar.google.com") or a.get("resource"):
            continue
        others += 1
    return others > 0
