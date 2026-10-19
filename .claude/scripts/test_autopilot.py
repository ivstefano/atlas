#!/usr/bin/env python3
"""Offline tests for the meeting autopilot fixes (no LLM, no Asana/HubSpot, no notifications, temp dirs only).

    /Users/iris/Documents/Cognion/atlas/.venv/bin/python .claude/scripts/test_autopilot.py
"""
import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
import zoneinfo
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import approval_executors as X  # noqa: E402
import approval_queue as Q  # noqa: E402
import autopilot_common as AC  # noqa: E402
import meeting_autopilot as A  # noqa: E402

SOFIA = zoneinfo.ZoneInfo("Europe/Sofia")


def at(h, m=0, day=19):
    return dt.datetime(2026, 10, day, h, m, tzinfo=SOFIA)


class Tmp(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="aptest_"))
        self._saved = (A.DRY, A.RUN, A.DRY_RUN, A.NOTIFY_IN_DRY, Q.QUEUE, AC.load_config, A._NOW)
        A.DRY, A.RUN = self.tmp / "dry", self.tmp / "run"
        A.DRY_RUN, A.NOTIFY_IN_DRY = True, False
        AC.load_config = lambda: {}
        A.log = lambda *a, **k: None

    def tearDown(self):
        A.DRY, A.RUN, A.DRY_RUN, A.NOTIFY_IN_DRY, Q.QUEUE, AC.load_config, A._NOW = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)


class ParseJson(unittest.TestCase):
    def test_plain_fenced_prose_trailing_comma(self):
        self.assertEqual(A.parse_json('{"a": 1}'), {"a": 1})
        self.assertEqual(A.parse_json('```json\n{"a": 1}\n```'), {"a": 1})
        self.assertEqual(A.parse_json('Here it is:\n```json\n{"a": [1, 2,],}\n```\nDone.'), {"a": [1, 2]})
        self.assertEqual(A.parse_json('Sure. {"a": {"b": 2}} trailing words'), {"a": {"b": 2}})

    def test_truncated_never_returns_a_nested_object(self):
        t = '{"status_entry": "## 2026-10-16\\n- x", "email": {"to": ["a@b.c"]}, "actions": [{"type": "sow", "what": "cut he'
        with self.assertRaises(ValueError):
            A.parse_json(t)
        d = A.parse_json(t, repair=True)
        self.assertTrue(d["_repaired"])
        self.assertEqual(d["email"], {"to": ["a@b.c"]})
        self.assertTrue(d["status_entry"].startswith("## 2026-10-16"))

    def test_sulzer_shape_is_repairable(self):
        """Shape of the 2026-10-18 Sulzer failure: 7000-token answer cut inside actions[].details.scope."""
        raw = ('{"status_entry":"## 2026-10-16\\n- What happened: Teams call (Piyush).\\n- Stage: pre-scoping",'
               '"artefacts":[],"email":{"skip_reason":null,"to":["piyush@sulzer.com"],"subject":"Next steps","body":"Hi Piyush,"},'
               '"slack":{"thread":"Sulzer","text":"Call done"},"actions":[{"type":"sow","what":"Revised doc","owner":"Ivo / Jordan",'
               '"jordan_owned":false,"details":{"scope":"Material master pilot"}},{"type":"data_request","what":"Ask Piyush for a rough '
               'list","owner":"Ivo","details":{"scope":"System list')
        with self.assertRaises(ValueError):
            A.parse_json(raw)
        d = A.repair_truncated_json(raw)
        self.assertTrue(d["status_entry"].startswith("## 2026-10-16"))
        self.assertEqual(d["email"]["to"], ["piyush@sulzer.com"])
        self.assertEqual(d["actions"][0]["type"], "sow")


class DigestJson(Tmp):
    def run_with(self, answers):
        calls = []

        def fake_llm(step, key, system, prompt, max_tokens=2000):
            txt, stop = answers[len(calls)]
            calls.append((max_tokens, prompt[-200:]))
            A.LAST_STOP = stop
            return txt
        A.llm = fake_llm
        dd = self.tmp / "dd"
        dd.mkdir()
        return A.digest_json("k", dd, "PROMPT"), calls, dd

    def test_cut_off_retry_gets_bigger_cap(self):
        good = '{"status_entry": "## d\\n- a\\n- b", "email": {}}'
        (d, why), calls, dd = self.run_with([('{"status_entry": "## d\\n- a', "max_tokens"), (good, "end_turn")])
        self.assertIsNone(why)
        self.assertEqual(d["email"], {})
        self.assertEqual([c[0] for c in calls], [16000, 24000])
        self.assertIn("cut off", calls[1][1])
        self.assertEqual(len(list(dd.glob("digest_raw_*.txt"))), 2)

    def test_both_cut_off_uses_repair_when_status_complete(self):
        cut = '{"status_entry": "## d\\n- a\\n- b", "email": {"to": [], "body": "Hi Pi'
        (d, why), _, _ = self.run_with([(cut, "max_tokens"), (cut, "max_tokens")])
        self.assertIsNone(why)
        self.assertTrue(d["_repaired"])

    def test_cut_inside_status_entry_is_rejected(self):
        cut = '{"status_entry": "## d\\n- a\\n- half a sent'
        (d, why), _, _ = self.run_with([(cut, "max_tokens"), (cut, "max_tokens")])
        self.assertIsNone(d)
        self.assertEqual(why, "bad json")


class QuietHours(Tmp):
    def test_window(self):
        self.assertIsNone(AC.quiet_until(at(18, 59)))
        self.assertEqual(AC.quiet_until(at(19, 0)), at(8, 0, day=20))
        self.assertEqual(AC.quiet_until(at(23, 30)), at(8, 0, day=20))
        self.assertEqual(AC.quiet_until(at(7, 59)), at(8, 0))
        self.assertIsNone(AC.quiet_until(at(8, 0)))
        AC.load_config = lambda: {"quiet_hours": {"off": True}}
        self.assertIsNone(AC.quiet_until(at(22, 0)))

    def test_notify_held_then_flushed_once(self):
        sent = []
        A.set_now(at(19, 30))
        A.notify("Digest ready: X", "2 drafts")
        A.notify("Digest updated: X", "2 drafts")
        self.assertEqual(len(A.deferred_path().read_text().splitlines()), 2)
        real_notify = A.notify
        A.notify = lambda title, msg, url=None, group=None, urgent=False: sent.append((title, msg, urgent))
        try:
            A.set_now(at(7, 0, day=20))
            self.assertEqual(A.flush_deferred(), 0)          # still quiet
            A.set_now(at(8, 2, day=20))
            self.assertEqual(A.flush_deferred(), 2)
            self.assertEqual(A.flush_deferred(), 0)          # popped
        finally:
            A.notify = real_notify
        self.assertEqual(len(sent), 1)
        self.assertTrue(sent[0][0].startswith("2 updates held overnight") and sent[0][2])

    def test_urgent_bypasses(self):
        A.set_now(at(19, 30))
        A.notify("Brief ready: late call", "Starts 19:42", urgent=True)
        self.assertFalse(A.deferred_path().exists())


class Queue(Tmp):
    def test_queue_add_pending_and_done_paths(self):
        """Bug (a): the pre-commit queue_add called approval_queue.add(item_dict). Every path must hit the real API."""
        A.set_now(at(15, 0))
        A.queue_add("k__email", "gmail_draft", "Follow-up", "Hi", {"to": ["a@b.c"]}, "sulzer", [{"label": "t", "ref": "x"}])
        A.queue_status_done("session:abcd1234:sulzer", "sulzer", "## 2026-10-19\n- x", "dry-run", "STATUS logged", source="session-hook")
        A.queue_status_done("session:abcd1234:sulzer", "sulzer", "## 2026-10-19\n- y", "dry-run", "STATUS logged", source="session-hook")
        items = Q.list_items()
        self.assertEqual(sorted(i["kind"] for i in items), ["gmail_draft", "status_entry"])
        st = next(i for i in items if i["kind"] == "status_entry")
        self.assertEqual((st["status"], st["source"], st["body"]), ("done", "session-hook", "## 2026-10-19\n- y"))
        self.assertTrue(all("surface_at" not in i for i in items))

    def test_items_created_in_quiet_hours_are_held(self):
        A.set_now(at(20, 15))
        A.queue_add("k__slack", "slack_post", "Post", "text", {}, "sulzer")
        it = Q.list_items()[0]
        self.assertEqual(it["surface_at"][:16], "2026-10-20T08:00")
        self.assertFalse(Q.visible(it, now=at(7, 59, day=20)))
        self.assertTrue(Q.visible(it, now=at(8, 0, day=20)))
        self.assertEqual(Q.pending_count(visible_only=False), 1)

    def test_add_default_uses_real_clock(self):
        Q.QUEUE = self.tmp / "q2"
        AC.load_config = lambda: {"quiet_hours": {"from": "00:00", "until": "23:59"}}
        it = Q.add("post-call", "x", "note", "t", "b")
        self.assertIn("surface_at", it)
        AC.load_config = lambda: {"quiet_hours": {"off": True}}
        self.assertNotIn("surface_at", Q.add("post-call", "x", "note", "t2", "b"))


class Asana(Tmp):
    TOOLS = ["mcp__asana__add_comment", "mcp__asana__create_project", "mcp__asana__create_task_from_template",
             "mcp__asana__create_tasks", "mcp__asana__delete_task", "mcp__asana__get_attachments",
             "mcp__asana__get_portfolio", "mcp__asana__get_task", "mcp__asana__get_tasks", "mcp__asana__get_project",
             "mcp__asana__search_tasks", "mcp__asana__update_project", "mcp__asana__update_tasks"]

    def test_tool_filter_least_privilege(self):
        ro = AC.asana_filter(self.TOOLS).split(",")
        self.assertEqual(ro, ["mcp__asana__get_project", "mcp__asana__get_task", "mcp__asana__get_tasks", "mcp__asana__search_tasks"])
        self.assertEqual(set(AC.asana_filter(self.TOOLS, ["complete"]).split(",")) - set(ro), {"mcp__asana__update_tasks"})
        self.assertEqual(set(AC.asana_filter(self.TOOLS, ["create"]).split(",")) - set(ro), {"mcp__asana__create_tasks"})
        for op in ("complete", "create", "update", "update_pipeline"):
            self.assertNotIn("delete", AC.asana_filter(self.TOOLS, [op]))
            self.assertNotIn("update_project", AC.asana_filter(self.TOOLS, [op]))

    def test_spec_validation(self):
        ok = X.asana_spec('{"op": "complete", "section": "Garrett", "task": "⏳ PoC Execution", "task_gid": "1219600285347494"}')
        self.assertEqual(ok["op"], "complete")
        for bad in ('{"op": "delete", "section": "G", "task": "x"}', '{"op": "create", "section": "G"}',
                    '{"op": "complete", "section": "G"}', '{"op": "complete", "section": "G", "task": "x", "project": "1"}',
                    '{"op": "create", "section": "G", "name": "x", "assignee": "jordan@gmail.com"}', "not json"):
            with self.assertRaises(ValueError):
                X.asana_spec(bad)
        s = X.asana_spec('{"op": "create", "section": "G", "name": "📅 Kickoff — Tue", "due_on": "2026-11-03", "assignee": "me"}')
        self.assertEqual(s["name"], "📅 Kickoff, Tue")
        find, act = X.asana_instructions(X.asana_spec('{"op": "update_pipeline", "section": "G", "task": "[PIPELINE] G", "stage": "Discovery"}'))
        self.assertIn("never change them", act)

    def test_split_flags_jordan_commercial(self):
        snap = ("### Asana section: Garrett\n- 1 | [PIPELINE] Garrett | open | Ivo Stefanov | due -\n"
                "- 2 | Send revised quote | open | Jordan Ryken | due 2026-10-22")
        props = [
            {"op": "complete", "section": "Garrett", "task": "⏳ PoC Execution", "task_gid": None, "reason": "done"},
            {"op": "create", "section": "Garrett", "name": "Send pricing for bridge phase", "reason": "asked"},
            {"op": "update", "section": "Garrett", "task": "Send revised quote", "due_on": "2026-10-30"},
            {"op": "create", "section": "Garrett", "name": "Ivo: architecture one-pager", "assignee": "Ivo", "due_on": "2026-10-24"},
            {"op": "create", "section": "Garrett", "name": "x", "jordan_owned": True},
            {"op": "explode", "section": "Garrett"},
        ]
        ok, jordan = A.asana_split(props, snap)
        self.assertEqual([s.get("task") or s.get("name") for s in ok], ["⏳ PoC Execution", "Ivo: architecture one-pager"])
        self.assertEqual(ok[1]["assignee"], "me")
        self.assertEqual(len(jordan), 3)

    def test_queue_asana_items_and_supersede(self):
        A.set_now(at(15, 0))
        specs = [X.asana_spec('{"op": "complete", "section": "Garrett", "task": "⏳ PoC Execution"}'),
                 X.asana_spec('{"op": "create", "section": "Garrett", "name": "📅 Kickoff", "due_on": "2026-11-03"}')]
        self.assertEqual(A.queue_asana("m1", specs, "garrett", []), 2)
        items = Q.list_items("pending")
        self.assertEqual({i["kind"] for i in items}, {"asana"})
        self.assertEqual(json.loads(next(i for i in items if "Kickoff" in i["title"])["body"])["due_on"], "2026-11-03")
        A.queue_asana("m1", specs[:1], "garrett", [])          # final digest dropped one proposal
        self.assertEqual(len(Q.list_items("pending")), 1)
        self.assertEqual(len(Q.list_items("rejected")), 1)

    def test_executor_uses_only_needed_tools_and_reports(self):
        """approval_executors.execute(kind=asana) with a fake headless claude: no real Asana call."""
        seen = {}
        real = (AC.mcp_tools, AC.claude_headless, X.LOG)
        X.LOG = self.tmp / "executor.log"
        AC.mcp_tools = lambda name, refresh=False, max_age_days=7: self.TOOLS

        def fake(prompt, names, allowed, **kw):
            seen.update(prompt=prompt, names=names, allowed=allowed)
            return 'Done.\n{"ok": true, "task_gid": "1219600285347494", "did": "completed PoC Execution"}', 0.004
        AC.claude_headless = fake
        try:
            item = {"id": "x", "kind": "asana", "target": {},
                    "body": '{"op": "complete", "section": "Garrett", "task": "⏳ PoC Execution"}'}
            res = X.execute(item)
            self.assertIn("completed PoC Execution", res["result"])
            self.assertTrue(res["link"].endswith("/1219600285347494"))
            self.assertEqual(seen["names"], ["asana"])
            self.assertIn("mcp__asana__update_tasks", seen["allowed"])
            self.assertNotIn("delete", seen["allowed"])
            self.assertNotIn("create", seen["allowed"])
            self.assertIn("1214855342290138", seen["prompt"])
            AC.claude_headless = lambda *a, **k: ('{"ok": false, "did": "no unique task"}', 0.003)
            with self.assertRaises(RuntimeError):
                X.execute(item)
            AC.mcp_tools = lambda name, refresh=False, max_age_days=7: []
            with self.assertRaisesRegex(RuntimeError, "not authenticated"):
                X.execute(item)
        finally:
            AC.mcp_tools, AC.claude_headless, X.LOG = real

    def test_section_guard(self):
        A._ALIASES = {"intertek": {"titles": ["Intertek"]}, "garrett": {"titles": ["Garrett"]},
                      "db-infrago": {"titles": ["DB InfraGO", "Deutsche Bahn"]}}
        self.assertFalse(A.section_matches("DeutscheBahn InfraGO", "intertek"))
        self.assertTrue(A.section_matches("Garrett", "garrett"))
        self.assertTrue(A.section_matches("DeutscheBahn InfraGO", "db-infrago"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
