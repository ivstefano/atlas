#!/usr/bin/env python3
"""Tests for confidence-decay reconciliation in state_flush.py.

Pure-function tests, no Haiku call. Run: python3 test_state_decay.py
Covers the marker math, fuzzy matching across reworded facts, sort order,
the trial 'never delete' guarantee, and the prune behaviour once enabled.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_flush as sf  # noqa: E402


def _state(*dre_bullets: str) -> str:
    body = "\n".join(dre_bullets)
    return f"""# STATE: t
last_session: x
last_tab: A

## Now
n

## Next action
na

## Open threads
- ot

## Don't re-explain
{body}
"""


PASS, FAIL = 0, 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}")


def counts(rendered):
    """rendered block -> {text_prefix: count}, keyed loosely for assertions."""
    out = {}
    for c, t in [(int(b.split(")")[0].split("c")[1]), b.split(") ", 1)[1])
                 for b in rendered.splitlines() if b.strip()]:
        out[t] = c
    return out


def test_new_fact_starts_c1():
    prior = _state("- (c3) alpha host is 1.2.3.4")
    current = _state("- (c3) alpha host is 1.2.3.4", "- (c1) beta is a new thing")
    rendered, stats = sf.reconcile_dre(prior, current)
    c = counts(rendered)
    check("carried fact increments c3->c4", c.get("alpha host is 1.2.3.4") == 4)
    check("new fact is c1", c.get("beta is a new thing") == 1)
    check("stats new==1", stats["new"] == 1)


def test_reworded_fact_matches():
    prior = _state("- (c2) Flush calls claude -p --model haiku from cwd /tmp")
    # reworded, Haiku dropped the marker entirely -> parsed as c1, should still match
    current = _state("- The flush runs a headless claude -p haiku call in /tmp")
    rendered, stats = sf.reconcile_dre(prior, current)
    c = counts(rendered)
    check("reworded fact matched & incremented to c3", list(c.values()) == [3])
    check("reworded counted as reinforced, not new", stats["new"] == 0)


def test_sort_high_to_low():
    prior = _state("- (c1) low", "- (c5) high", "- (c3) mid")
    current = _state("- (c1) low", "- (c5) high", "- (c3) mid")
    rendered, _ = sf.reconcile_dre(prior, current)
    order = [b.split(") ", 1)[1] for b in rendered.splitlines() if b.strip()]
    check("sorted high->low", order == ["high", "mid", "low"])


def test_trial_never_deletes():
    # PRUNE_ENABLED is False in trial. A c1 fact that is NOT reinforced
    # (absent from prior) must still survive.
    assert sf.PRUNE_ENABLED is False, "trial expects pruning OFF"
    prior = _state("- (c4) established fact")
    current = _state("- (c4) established fact", "- (c1) shaky one-off fact")
    rendered, stats = sf.reconcile_dre(prior, current)
    c = counts(rendered)
    check("trial keeps shaky c1 fact (no delete)", "shaky one-off fact" in c)
    check("trial pruned count is 0", stats["pruned"] == 0)


def test_prune_when_enabled():
    # Temporarily flip pruning on to prove the rule works for the post-trial state.
    sf.PRUNE_ENABLED = True
    try:
        prior = _state("- (c4) established fact")
        # 'shaky' is new (c1) and unreinforced -> should be pruned once enabled.
        # 'established' is reinforced -> survives.
        current = _state("- (c4) established fact", "- (c1) shaky one-off fact")
        rendered, stats = sf.reconcile_dre(prior, current)
        c = counts(rendered)
        check("pruned: shaky c1 unreinforced removed", "shaky one-off fact" not in c)
        check("pruned: established survives", "established fact" in c)
        check("prune stats count==1", stats["pruned"] == 1)

        # A brand-new fact that IS its own first sighting but reinforced same
        # session can't happen; but a c1 fact present in prior (reinforced) must
        # survive even at low count.
        prior2 = _state("- (c1) borderline fact")
        current2 = _state("- (c1) borderline fact")
        rendered2, _ = sf.reconcile_dre(prior2, current2)
        check("pruned-mode keeps reinforced low-c fact", "borderline fact"
              in counts(rendered2))
    finally:
        sf.PRUNE_ENABLED = False


def test_apply_decay_splices_section():
    prior = _state("- (c2) keep me")
    current = _state("- (c2) keep me", "- (c1) and me")
    spliced, _ = sf.apply_decay(prior, current)
    check("splice preserves other sections", "## Next action" in spliced
          and "## Open threads" in spliced)
    check("splice rewrote DRE with markers", "(c3) keep me" in spliced)
    check("splice kept new fact", "(c1) and me" in spliced)


def test_missing_section_is_safe():
    nostate = "# STATE: t\nlast_session: x\n\n## Now\nn\n"
    spliced, stats = sf.apply_decay(nostate, nostate)
    check("no DRE section -> returns text unchanged", spliced == nostate)
    check("no DRE section -> 0 facts", stats["facts"] == 0)


if __name__ == "__main__":
    for fn in [
        test_new_fact_starts_c1,
        test_reworded_fact_matches,
        test_sort_high_to_low,
        test_trial_never_deletes,
        test_prune_when_enabled,
        test_apply_decay_splices_section,
        test_missing_section_is_safe,
    ]:
        print(fn.__name__)
        fn()
    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
