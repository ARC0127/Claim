"""Explicit UTF-8 artifact validation, without host skills or third-party packages.

python tools/validate.py [--installed PATH]
python tools/validate.py --skill PATH
Checks files and literal contracts, not model behavior or mathematics.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BOM = b"\xef\xbb\xbf"
COACH = "references/theory-coach.md"
REQUIRED = {"SKILL.md", "agents/openai.yaml", COACH,
            "references/obligation-feedback.md", "references/claim-review.md",
            "references/claim-record.md"}
HEADINGS = ("你刚才表达了什么", "我如何形式化", "当前最大歧义", "一个需要你亲自回答的问题")
STATUS = ("阶段 Sx · GATE OPEN", "模式：DEEP_DIVE · NO ADVANCE",
          "检索：FRESH_LITERATURE_PASS · PRIOR SOURCES UNCONFIRMED")
TEXT = {".md", ".yaml", ".yml", ".json", ".txt", ".py", ".ps1", ".svg", ".html", ".css"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read_version(root):
    version = read_text(root / "VERSION").strip()
    require(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version), "Invalid release version")
    return version

def read_text(path, bom=False):
    data = path.read_bytes()
    require(data.startswith(BOM) == bom, f"BOM policy mismatch: {path}")
    text = data.decode("utf-8-sig", errors="strict")
    require(not re.search(r"[\u0000\ufffd\ue000-\uf8ff]", text), f"Damaged text: {path}")
    return text

def safe_file(root, relative):
    p = PurePosixPath(relative)
    require(not p.is_absolute() and ".." not in p.parts and "\\" not in relative
            and ":" not in relative, f"Unsafe package path: {relative}")
    target = root.joinpath(*p.parts)
    require(target.resolve().is_relative_to(root.resolve()), f"Path leaves root: {relative}")
    require(target.is_file() and not target.is_symlink(), f"Missing file or symlink: {relative}")
    return target

def check_skill(skill):
    actual = {p.relative_to(skill).as_posix() for p in skill.rglob("*") if p.is_file()}
    require(actual == REQUIRED, f"Skill file set differs: missing={sorted(REQUIRED-actual)}, extra={sorted(actual-REQUIRED)}")
    contents = {rel: read_text(safe_file(skill, rel), rel == COACH) for rel in sorted(actual)}
    entry = contents["SKILL.md"]
    require(entry.startswith("---\n"), "SKILL.md must begin with YAML frontmatter")
    front = entry.split("---", 2)[1]
    require(re.search(r"^name: claim$", front, re.M), "Missing skill name")
    require(re.search(r"^description: .+", front, re.M), "Missing description")
    require(all(x in contents[COACH] for x in HEADINGS + STATUS), "Canonical Chinese template missing")
    for rel in ("SKILL.md", COACH):
        require("ENCODING_CONTRACT: UTF-8" in contents[rel]
                and "MOJIBAKE_POLICY: FAIL_CLOSED_AND_REREAD" in contents[rel], f"Encoding preflight missing: {rel}")
    require("$claim" in contents["agents/openai.yaml"], "UI prompt must invoke $claim")
    for rel, text in contents.items():
        require(not re.search(r"zyr-[a-z0-9-]+|theory-claim-audit|F:[/\\]Archives|D:[/\\]codex", text, re.I),
                f"External skill or private local dependency in {rel}")
    return actual

def check_links(path, root):
    text = read_text(path)
    targets = re.findall(r"!?\[[^\]\n]*\]\(([^)\s]+)\)", text)
    targets += re.findall(r'(?:src|href)="([^"<>]+)"', text)
    for target in targets:
        if re.match(r"[a-z]+:|#|//", target, re.I):
            continue
        rel = target.split("#", 1)[0]
        if rel:
            resolved = (path.parent / rel).resolve()
            require(resolved.is_relative_to(root.resolve()) and resolved.is_file(), f"Broken local link: {path.name} -> {target}")

def check_repo(root, installed=None):
    skill_files = check_skill(root / "claim")
    manifest = json.loads(read_text(root / "manifest.json"))
    version = read_version(root)
    require(manifest["internal_version"] == version, "Manifest/VERSION mismatch")
    require(manifest["archive"] == f"dist/Claim-{version}.zip", "Archive version mismatch")
    require(manifest["entrypoint"] == "claim/SKILL.md" and manifest["archive_layout"] == "claim/", "Wrong package entry/layout")
    core = manifest["core_files"]
    require(len(core) == len(set(core)) and set(core) == {"claim/" + p for p in skill_files}, "Manifest core file set differs")
    require(version in read_text(root / "README.md"), "README does not name current version")
    public = [root / p for p in ("README.md", "VERSION", "manifest.json", ".gitattributes", ".gitignore")]
    for folder in ("claim", "docs", "tools", "tests"):
        public += [p for p in (root / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    for path in public:
        if path.suffix in TEXT or path.name in {"VERSION", ".gitattributes", ".gitignore"}:
            read_text(path, path == root / "claim" / COACH)
        if path.suffix in {".md", ".html", ".svg"} and not path.is_relative_to(root / "claim"):
            check_links(path, root)
    sums = {}
    for line in read_text(root / "dist/SHA256SUMS.txt").splitlines():
        digest, rel = line.split("  ", 1)
        require(re.fullmatch(r"[0-9a-f]{64}", digest), "Invalid checksum row")
        require(rel not in sums, "Duplicate checksum target")
        require(hashlib.sha256(safe_file(root, rel).read_bytes()).hexdigest() == digest, f"Checksum mismatch: {rel}")
        sums[rel] = digest
    require(set(core + [manifest["archive"]]).issubset(sums), "Required checksums missing")
    with zipfile.ZipFile(safe_file(root, manifest["archive"])) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and set(names) == set(core), "ZIP has missing, extra or duplicate entries")
        require(archive.testzip() is None, "ZIP CRC failed")
        for rel in core:
            require(archive.read(rel) == safe_file(root, rel).read_bytes(), f"ZIP content differs: {rel}")
    if installed is not None:
        check_skill(installed)
        for rel in skill_files:
            require((installed / rel).read_bytes() == (root / "claim" / rel).read_bytes(), f"Installed file differs: {rel}")
    return version

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--skill", type=Path)
    parser.add_argument("--installed", type=Path)
    args = parser.parse_args()
    try:
        if args.skill:
            check_skill(args.skill)
            print("PASS: standalone Claim skill, UTF-8 and local route files")
        else:
            version = check_repo(args.repo, args.installed)
            print(f"PASS: Claim {version}, UTF-8, links, manifest, checksums and exact ZIP")
            if args.installed:
                print("PASS: installed skill matches source bytes")
        print("Scope: structural/artifact checks only; no model or learning effect certified.")
        return 0
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
