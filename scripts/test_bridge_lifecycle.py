#!/usr/bin/env python3
"""Focused tests for the Codex thread lifecycle used by the local bridge."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("zotero_codex_bridge", PROJECT_ROOT / "bridge" / "server.py")
assert SPEC and SPEC.loader
SERVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER)


class FakeApp(SERVER.CodexAppServer):
    def __init__(self, archived: set[str] | None = None, missing: set[str] | None = None):
        super().__init__(Path("/unused/codex-app-server"))
        self.archived = set(archived or set())
        self.missing = set(missing or set())
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def request(self, method: str, params: dict[str, Any], timeout: float = 60) -> dict[str, Any]:
        self.calls.append((method, params))
        thread_id = params.get("threadId")
        if method == "thread/resume" and thread_id in self.archived:
            raise SERVER.BridgeError("thread is archived")
        if method == "thread/unarchive":
            if thread_id in self.missing:
                raise SERVER.BridgeError("no archived rollout found")
            self.archived.discard(thread_id)
            return {"thread": {"id": thread_id}}
        if method == "thread/archive":
            if thread_id in self.missing:
                raise SERVER.BridgeError("no rollout found")
            if thread_id in self.archived:
                raise SERVER.BridgeError("no rollout found")
            self.archived.add(thread_id)
            return {}
        if method == "thread/delete":
            self.archived.discard(thread_id)
            return {}
        if method == "turn/start":
            with self._state_lock:
                subscribers = list(self._subscribers.get(thread_id, set()))
            completed = {
                "method": "turn/completed",
                "params": {"threadId": thread_id, "turn": {"id": "turn-1", "status": "completed"}},
            }
            for subscriber in subscribers:
                subscriber.put(completed)
            return {"turn": {"id": "turn-1"}}
        return {}


class ThreadLifecycleTests(unittest.TestCase):
    def test_new_threads_use_non_interactive_app_server_source(self) -> None:
        self.assertEqual(SERVER.SESSION_SOURCE, "app-server")

    def test_web_search_mode_defaults_to_live_and_rejects_unknown_values(self) -> None:
        app = FakeApp()
        self.assertEqual(app.web_search_mode({}), "live")
        self.assertEqual(app.web_search_mode({"webSearchMode": "cached"}), "cached")
        self.assertEqual(app.web_search_mode({"webSearchMode": "disabled"}), "disabled")
        self.assertEqual(app.web_search_mode({"webSearchMode": "unexpected"}), "live")

    def test_archived_thread_is_unarchived_before_resume(self) -> None:
        app = FakeApp({"thread-1"})
        result = app._ensure_thread({"threadId": "thread-1", "cwd": "/tmp"})
        self.assertEqual(result, "thread-1")
        self.assertEqual(
            [method for method, _params in app.calls],
            ["thread/resume", "thread/unarchive", "thread/resume"],
        )
        resume_params = [params for method, params in app.calls if method == "thread/resume"]
        self.assertTrue(all(params["config"] == {"web_search": "live"} for params in resume_params))

    def test_resume_applies_selected_web_search_mode(self) -> None:
        app = FakeApp()
        result = app._ensure_thread(
            {"threadId": "thread-1", "cwd": "/tmp", "webSearchMode": "disabled"}
        )
        self.assertEqual(result, "thread-1")
        self.assertEqual(app.calls[0][1]["config"], {"web_search": "disabled"})

    def test_completed_turn_is_archived_and_unloaded(self) -> None:
        app = FakeApp()
        app._loaded_threads.add("thread-1")
        events = list(app.stream_chat({"threadId": "thread-1", "message": "test"}))
        self.assertEqual(events[-1]["type"], "done")
        self.assertIn("thread-1", app.archived)
        self.assertNotIn("thread-1", app._loaded_threads)

    def test_archiving_is_safe_to_retry(self) -> None:
        app = FakeApp({"thread-1"})
        app.archive_thread("thread-1")
        self.assertIn("thread-1", app.archived)
        self.assertEqual(
            [method for method, _params in app.calls],
            ["thread/archive", "thread/unarchive", "thread/archive"],
        )

    def test_missing_thread_is_already_absent_from_recent(self) -> None:
        app = FakeApp(missing={"thread-1"})
        app.archive_thread("thread-1")
        self.assertNotIn("thread-1", app._loaded_threads)

    def test_delete_discards_loaded_thread(self) -> None:
        app = FakeApp({"thread-1"})
        app._loaded_threads.add("thread-1")
        app.delete_thread("thread-1")
        self.assertNotIn("thread-1", app.archived)
        self.assertNotIn("thread-1", app._loaded_threads)


if __name__ == "__main__":
    unittest.main()
