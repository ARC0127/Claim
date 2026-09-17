"""Reproducible Claim ZIP: python tools/package.py --write or --check.

Only the current manifest archive and generated SHA256SUMS are written.
"""
import argparse
import hashlib
import io
import json
import sys
import zipfile
from validate import ROOT, check_skill, read_text, read_version, require, safe_file

def archive_bytes(root):
    files = check_skill(root / "claim")
    manifest = json.loads(read_text(root / "manifest.json"))
    version = read_version(root)
    require(manifest["internal_version"] == version, "Manifest/VERSION mismatch")
    require(manifest["archive"] == f"dist/Claim-{version}.zip", "Archive version mismatch")
    expected = {"claim/" + p for p in files}
    require(set(manifest["core_files"]) == expected and len(manifest["core_files"]) == len(expected), "Invalid core allowlist")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel in sorted(expected):
            item = zipfile.ZipInfo(rel, date_time=(2020, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, safe_file(root, rel).read_bytes())
    return manifest, output.getvalue()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        manifest, payload = archive_bytes(ROOT)
        target = ROOT / manifest["archive"]
        if args.write:
            target.parent.mkdir(exist_ok=True)
            require(target.parent.resolve().is_relative_to(ROOT.resolve()) and not target.is_symlink(), "Archive target leaves repository or is a symlink")
            target.write_bytes(payload)
            paths = sorted(manifest["core_files"]) + sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "dist").glob("Claim-*.zip"))
            rows = [f"{hashlib.sha256(safe_file(ROOT, rel).read_bytes()).hexdigest()}  {rel}" for rel in paths]
            (ROOT / "dist/SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
            print(f"Built {manifest['archive']} ({len(payload)} bytes)")
        else:
            require(target.read_bytes() == payload, "Archive differs from deterministic rebuild")
            print("PASS: deterministic archive rebuild matches")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
