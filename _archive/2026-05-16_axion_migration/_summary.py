#!/usr/bin/env python3
"""Generate _SUMMARY.md from the per-engagement _raw.json + a tally of placeholders."""
import json
import os
import subprocess
from pathlib import Path

OUT = Path("/Users/iris/Documents/atlas/_axion_audit")
AXION = Path("/Users/iris/Documents/Axion/scoping")

ACTIVE = ["postbank", "aumovio", "heineken", "welocalize", "garrett",
          "sms-group", "tandf", "agrolimen", "fresenius", "deutschebahn", "nhs"]
HALTED = ["alexfert", "shanghai-synocodes", "stepan", "aumovio-soft-impact",
          "hubspot", "cetin"]
EMPTY = ["ahli", "allianz", "aramco", "basamh", "brunela", "ciklum",
         "lifescience", "orion", "riyadbank"]
# Note: yettel was listed as empty in the brief but has substantial content (535 files)
# — audited separately and flagged under "anomalies"
ANOMALIES = ["yettel"]
# Halted reasons
HALTED_REASONS = {
    "alexfert": "war-paused",
    "shanghai-synocodes": "lost (price)",
    "stepan": "lost (no project)",
    "aumovio-soft-impact": "merged into Aumovio main",
    "hubspot": "internal IRIS exploration only",
    "cetin": "halted / no engagement",
}

# Tombstone check (does engagements/<co>/ exist?)
def has_engagement_tombstone(co: str) -> str:
    p = Path(f"/Users/iris/Documents/engagements/{co}")
    return "yes" if p.exists() else "no"


def human_size(n):
    n = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def folder_size(p: Path) -> int:
    if not p.exists():
        return 0
    try:
        r = subprocess.run(["du", "-sk", str(p)], capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            kb = int(r.stdout.split()[0])
            return kb * 1024
    except Exception:
        pass
    return 0


def folder_file_count(p: Path) -> int:
    if not p.exists():
        return 0
    try:
        r = subprocess.run(["find", str(p), "-type", "f"], capture_output=True, text=True, timeout=30)
        return len([l for l in r.stdout.splitlines() if l.strip()])
    except Exception:
        return 0


def main():
    raw = json.loads((OUT / "_raw.json").read_text())

    L = []
    L.append("# Axion audit — summary\n")
    L.append(f"_Generated {subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%MZ']).decode().strip()}._\n")

    # Active engagements
    L.append("## Active engagements (will migrate)\n")
    L.append("| Engagement | Axion size | Files | Drive cov | Orphans | data files | code files | output files | Action |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for co in ACTIVE:
        if co not in raw:
            # daikin/finom expected missing
            L.append(f"| {co} | (no Axion folder) | - | - | - | - | - | - | n/a (pre-scoping, never in Axion) |")
            continue
        r = raw[co]
        cov = (r["drive_matches"] / r["total_files"] * 100) if r["total_files"] else 0
        # Action recommendation
        if r["total_files"] < 50:
            action = "Phase 2 pilot (small)"
        elif r["orphan_count"] > 50:
            action = "Phase 3 (orphan-heavy)"
        else:
            action = "Phase 3"
        L.append(f"| {co} | {human_size(r['total_size'])} | {r['total_files']} | {cov:.0f}% | {r['orphan_count']} | {r['cat_counts']['data']} | {r['cat_counts']['code']} | {r['cat_counts']['output']} | {action} |")
    # Add daikin/finom rows
    for co in ("daikin", "finom"):
        L.append(f"| {co} | (no Axion folder) | - | - | - | - | - | - | n/a (pre-scoping, never in Axion) |")
    L.append("")

    # Halted/declined
    L.append("## Halted / declined (will delete in Phase 1)\n")
    L.append("| Engagement | Axion size | Files | Drive cov | Orphans | Reason | Tombstone in engagements/? |")
    L.append("|---|---|---|---|---|---|---|")
    for co in HALTED:
        if co not in raw:
            # hubspot, aumovio-soft-impact need to be measured ad-hoc
            sz = folder_size(AXION / co)
            nf = folder_file_count(AXION / co)
            L.append(f"| {co} | {human_size(sz)} | {nf} | n/a | n/a | {HALTED_REASONS.get(co, '?')} | {has_engagement_tombstone(co)} |")
            continue
        r = raw[co]
        cov = (r["drive_matches"] / r["total_files"] * 100) if r["total_files"] else 0
        L.append(f"| {co} | {human_size(r['total_size'])} | {r['total_files']} | {cov:.0f}% | {r['orphan_count']} | {HALTED_REASONS.get(co, '?')} | {has_engagement_tombstone(co)} |")
    L.append("")

    # Empty placeholders
    L.append("## Empty placeholders (will delete)\n")
    L.append("| Folder | Size | Files | Notes |")
    L.append("|---|---|---|---|")
    for co in EMPTY:
        sz = folder_size(AXION / co)
        nf = folder_file_count(AXION / co)
        # Quick peek
        note = ""
        if nf == 0:
            note = "truly empty"
        elif nf <= 2:
            files = subprocess.run(["find", str(AXION / co), "-type", "f"], capture_output=True, text=True, timeout=10).stdout.splitlines()
            note = " + ".join(os.path.basename(f) for f in files[:3])
        L.append(f"| {co} | {human_size(sz)} | {nf} | {note} |")
    L.append("")

    # Anomalies: listed as empty but actually has substantial content
    L.append("## Anomalies (listed as empty in brief, but has content)\n")
    L.append("| Engagement | Axion size | Files | Drive cov | Orphans | data | code | output | Note |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for co in ANOMALIES:
        if co not in raw:
            continue
        r = raw[co]
        cov = (r["drive_matches"] / r["total_files"] * 100) if r["total_files"] else 0
        L.append(f"| {co} | {human_size(r['total_size'])} | {r['total_files']} | {cov:.0f}% | {r['orphan_count']} | {r['cat_counts']['data']} | {r['cat_counts']['code']} | {r['cat_counts']['output']} | brief said empty, but contains a RAG pipeline + ~55 client docs; needs disposition decision |")
    L.append("")

    # Top-level Axion loose files (not engagement-specific)
    L.append("## Axion top-level loose files\n")
    L.append("| File | Size | Note |")
    L.append("|---|---|---|")
    for f in sorted(os.listdir(AXION)):
        full = AXION / f
        if full.is_file():
            try:
                sz = full.stat().st_size
            except OSError:
                continue
            if f.startswith("."):
                continue
            L.append(f"| {f} | {human_size(sz)} | top-level, decide per-file |")
    L.append("")

    # Cross-engagement findings
    audited = [co for co in ACTIVE + HALTED if co in raw]
    total_size = sum(raw[co]["total_size"] for co in audited)
    total_files = sum(raw[co]["total_files"] for co in audited)
    active_size = sum(raw[co]["total_size"] for co in ACTIVE if co in raw)
    active_files = sum(raw[co]["total_files"] for co in ACTIVE if co in raw)
    halted_size = sum(raw[co]["total_size"] for co in HALTED if co in raw)
    total_orphans = sum(raw[co]["orphan_count"] for co in audited)
    total_code_files = sum(raw[co]["cat_counts"]["code"] for co in audited)
    total_code_size = sum(raw[co]["cat_sizes"]["code"] for co in audited)
    total_output_files = sum(raw[co]["cat_counts"]["output"] for co in audited)
    total_output_size = sum(raw[co]["cat_sizes"]["output"] for co in audited)
    total_data_size = sum(raw[co]["cat_sizes"]["data"] for co in audited)

    most_code = max(audited, key=lambda c: raw[c]["cat_counts"]["code"])
    most_orphans = max(audited, key=lambda c: raw[c]["orphan_count"])

    L.append("## Cross-engagement findings\n")
    L.append(f"- Total Axion size audited: **{human_size(total_size)}** across {len(audited)} engagements ({total_files} files).")
    L.append(f"- Active engagements: {human_size(active_size)} across {active_files} files ({len([c for c in ACTIVE if c in raw])} engagements with Axion folders).")
    L.append(f"- Halted/declined (will delete): {human_size(halted_size)} across {sum(raw[c]['total_files'] for c in HALTED if c in raw)} files.")
    L.append(f"- Files needing upload-to-Drive-first (data orphans across all audited): **{total_orphans}** files.")
    L.append(f"- Total code files to move into engagement repos: **{total_code_files}** files ({human_size(total_code_size)}).")
    L.append(f"- Total output files (extraction results, deliverables): **{total_output_files}** files ({human_size(total_output_size)}) — should land in Drive iris-outputs/ or S3.")
    L.append(f"- Total client data (already-on-Drive + orphans): {human_size(total_data_size)} — bulk of the Axion footprint.")
    L.append(f"- Engagement with most code files: **{most_code}** ({raw[most_code]['cat_counts']['code']} files, {human_size(raw[most_code]['cat_sizes']['code'])}).")
    L.append(f"- Engagement with most data orphans: **{most_orphans}** ({raw[most_orphans]['orphan_count']} files).")
    L.append("")

    # Phase recommendation
    L.append("## Phase plan derived from audit\n")
    L.append("**Phase 1 — delete halted/declined + empty placeholders.** Confirm tombstones exist in `engagements/` for each before deleting. Items where the engagements/ tombstone is `no` need a tombstone written first.")
    L.append("")
    L.append("**Phase 2 — pilot migration (postbank).** 34 files, 9.7 MB, 100% non-orphan. Cleanest pilot: validates the migration script and the engagements/<co>/<stage>/extraction/ destination layout.")
    L.append("")
    L.append("**Phase 3 — batch migrate the active rest.** Per-engagement, in size order:")
    for co in sorted([c for c in ACTIVE if c in raw], key=lambda c: raw[c]["total_size"]):
        r = raw[co]
        cov = (r["drive_matches"] / r["total_files"] * 100) if r["total_files"] else 0
        L.append(f"- `{co}` — {human_size(r['total_size'])}, {r['total_files']} files, {r['orphan_count']} orphans, {cov:.0f}% drive cov.")
    L.append("")
    L.append("**Phase 4 — handle Axion loose top-level files** (Usage-based pricing xlsx, bbox_editor.html, root .DS_Store).")
    L.append("")
    L.append("## Read the per-engagement audits\n")
    for co in audited + [c for c in ANOMALIES if c in raw]:
        L.append(f"- [{co}](./{co}.md)")
    L.append("")
    (OUT / "_SUMMARY.md").write_text("\n".join(L) + "\n")
    print(f"wrote _SUMMARY.md  ({len(L)} lines)")


if __name__ == "__main__":
    main()
