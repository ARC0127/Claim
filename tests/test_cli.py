import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("claim_cli", Path(__file__).resolve().parents[1] / "claim/scripts/claim.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

class CLITests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows npm shim")
    def test_windows_native_npm_shim(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            native = root / "node_modules/@anthropic-ai/claude-code/bin/claude.exe"
            native.parent.mkdir(parents=True)
            native.touch()
            with patch.object(cli.shutil, "which", return_value=str(root / "claude.cmd")):
                self.assertEqual(cli.client_command("claude"), [str(native)])

    @unittest.skipUnless(os.name == "nt", "Windows npm shim")
    def test_windows_legacy_node_shim(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            script = root / "node_modules/@anthropic-ai/claude-code/cli.js"
            script.parent.mkdir(parents=True)
            script.touch()
            with patch.object(cli.shutil, "which", side_effect=lambda name: str(root / "claude.cmd") if name == "claude" else "node.exe"):
                self.assertEqual(cli.client_command("claude"), ["node.exe", str(script)])

    def test_prompt_modes_load_relevant_protocol(self):
        for mode, marker in (("coach", "S5a"), ("review", "Review one scientific claim"), ("proof", "Prove2Me")):
            with self.subTest(mode=mode):
                self.assertIn(marker, cli.context(mode, "我的主张"))

    def test_export_utf8_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "context.md"
            args = ["prompt", "--request", "中文主张", "--output", str(path)]
            self.assertEqual(cli.main(args), 0)
            original = path.read_bytes()
            self.assertIn("中文主张", original.decode("utf-8"))
            self.assertEqual(cli.main(args), 1)
            self.assertEqual(path.read_bytes(), original)

    def test_client_request_remains_one_argument(self):
        request = '中文 & echo bad; $(bad) "quoted"'
        with patch.object(cli, "client_command", return_value=["native.exe"]):
            for client in ("claude", "codex"):
                plan = cli.launch_plan(client, "coach", request)
                self.assertTrue(plan[-1].endswith(request))
                self.assertEqual(plan[-2], "--")
                self.assertNotIn("--model", plan)
                self.assertFalse(any("skip-permission" in x for x in plan))

    def test_missing_client_is_visible(self):
        with patch.object(cli.shutil, "which", return_value=None):
            with self.assertRaisesRegex(ValueError, "not on PATH"):
                cli.client_command("claude")

    def test_dry_run_does_not_start_client(self):
        with patch.object(cli, "client_command", return_value=["native.exe"]), patch.object(cli.subprocess, "run") as run:
            self.assertEqual(cli.main(["run", "--client", "claude", "--request", "test", "--dry-run"]), 0)
            run.assert_not_called()

    def test_run_preserves_client_exit_and_no_shell(self):
        with patch.object(cli, "client_command", return_value=["native.exe"]), patch.object(cli.subprocess, "run") as run:
            run.return_value.returncode = 7
            self.assertEqual(cli.main(["run", "--client", "claude", "--request", "test"]), 7)
            self.assertFalse(run.call_args.kwargs["shell"])

    def test_optional_zyr_presence_not_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            self.assertEqual(cli.doctor(path)["zyr_status"], "NOT_FOUND_OPTIONAL")
            (path / "SKILL.md").write_text("test", encoding="utf-8")
            self.assertEqual(cli.doctor(path)["zyr_status"], "ENTRY_PRESENT_NOT_EXECUTED")

if __name__ == "__main__":
    unittest.main()
