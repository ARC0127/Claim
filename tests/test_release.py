"""Artifact regressions only; these tests do not execute an LLM tutor."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import package
import validate


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="claim-release-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("claim", "docs", "dist"):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ("README.md", "README.zh-CN.md", "VERSION", "manifest.json", ".gitattributes", ".gitignore"):
            shutil.copy2(ROOT / name, self.root / name)

    def test_clean_repo_and_isolated_skill(self):
        self.assertEqual(validate.check_repo(self.root), "0.3.0")
        self.assertEqual(validate.check_skill(self.root / "claim"), validate.REQUIRED)

    def test_invalid_utf8_rejected(self):
        target = self.root / "claim/SKILL.md"
        target.write_bytes(target.read_bytes() + b"\xff")
        with self.assertRaises(UnicodeDecodeError):
            validate.check_skill(self.root / "claim")

    def test_missing_coach_bom_rejected(self):
        target = self.root / "claim" / validate.COACH
        target.write_bytes(target.read_bytes()[3:])
        with self.assertRaisesRegex(ValueError, "BOM policy"):
            validate.check_skill(self.root / "claim")

    def test_replacement_and_private_use_rejected(self):
        target = self.root / "claim/SKILL.md"
        original = target.read_bytes()
        for char in ("\ufffd", "\ue123"):
            with self.subTest(char=ascii(char)):
                target.write_bytes(original + char.encode("utf-8"))
                with self.assertRaisesRegex(ValueError, "Damaged text"):
                    validate.check_skill(self.root / "claim")

    def test_missing_bundled_route_rejected(self):
        (self.root / "claim/references/claim-review.md").unlink()
        with self.assertRaisesRegex(ValueError, "Skill file set"):
            validate.check_skill(self.root / "claim")

    def test_external_skill_route_rejected(self):
        target = self.root / "claim/SKILL.md"
        target.write_bytes(target.read_bytes() + b"\nLoad D:/private/skills/proof-helper/SKILL.md.\n")
        with self.assertRaisesRegex(ValueError, "External skill"):
            validate.check_skill(self.root / "claim")

    def test_canonical_heading_damage_rejected(self):
        target = self.root / "claim" / validate.COACH
        target.write_bytes(target.read_bytes().replace(validate.HEADINGS[0].encode(), b"broken"))
        with self.assertRaisesRegex(ValueError, "Canonical Chinese"):
            validate.check_skill(self.root / "claim")

    def test_rebuild_deterministic_and_exact(self):
        manifest, first = package.archive_bytes(self.root)
        _, second = package.archive_bytes(self.root)
        self.assertEqual(first, second)
        self.assertEqual(first, (self.root / manifest["archive"]).read_bytes())

    def test_manifest_extra_and_duplicate_rejected(self):
        target = self.root / "manifest.json"
        original = json.loads(target.read_text(encoding="utf-8"))
        for extra in ("../outside.txt", original["core_files"][0]):
            with self.subTest(extra=extra):
                changed = dict(original, core_files=original["core_files"] + [extra])
                target.write_text(json.dumps(changed), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "allowlist"):
                    package.archive_bytes(self.root)

    def test_version_path_injection_rejected(self):
        (self.root / "VERSION").write_text("../../outside", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid release version"):
            package.archive_bytes(self.root)

    def test_zip_extra_rejected_even_with_updated_checksum(self):
        rel = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))["archive"]
        target = self.root / rel
        with zipfile.ZipFile(target, "a") as archive:
            archive.writestr("claim/private-note.txt", "must not ship")
        sums = self.root / "dist/SHA256SUMS.txt"
        rows = sums.read_text(encoding="utf-8").splitlines()
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        sums.write_text("\n".join(digest + "  " + rel if row.endswith("  " + rel) else row for row in rows) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "ZIP has"):
            validate.check_repo(self.root)

    def test_installed_difference_rejected(self):
        installed = self.root / "installed"
        shutil.copytree(self.root / "claim", installed)
        target = installed / "references/claim-record.md"
        target.write_bytes(target.read_bytes() + b"\nChanged locally.\n")
        with self.assertRaisesRegex(ValueError, "Installed file differs"):
            validate.check_repo(self.root, installed)

    def test_broken_readme_link_rejected(self):
        target = self.root / "README.md"
        target.write_bytes(target.read_bytes() + b"\n[missing](docs/missing.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken local link"):
            validate.check_repo(self.root)


if __name__ == "__main__":
    unittest.main()
