"""Claim: local context export and native interactive client launcher (Python 3.10+)."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1]
MODES = {
    "coach": ["references/theory-coach.md", "references/obligation-feedback.md"],
    "review": ["references/claim-review.md", "references/obligation-feedback.md"],
    "proof": ["references/formal-proof.md", "references/claim-review.md"],
}

def text(path):
    return path.read_text(encoding="utf-8-sig")

def version():
    return text(SKILL / "VERSION").strip()

def context(mode, request):
    parts = ["# Claim " + version(), "Selected mode: " + mode]
    for name in ["SKILL.md"] + MODES[mode]:
        parts.append("\n## Source: " + name + "\n" + text(SKILL / name))
    parts.append("\n## User request\n" + request)
    return "\n".join(parts) + "\n"

def client_command(client):
    executable = shutil.which(client)
    if not executable:
        raise ValueError(client + " is not on PATH; install the native client or use prompt --output")
    # Resolve the executable behind the official Windows npm shim. Do not feed a user's
    # request through cmd.exe, shell=True or a string-built shell command.
    if os.name == "nt" and Path(executable).suffix.lower() in {".cmd", ".bat", ".ps1"}:
        package = Path(executable).parent / "node_modules/@anthropic-ai/claude-code"
        native_cli = package / "bin/claude.exe"
        if client == "claude" and native_cli.is_file():
            return [str(native_cli)]
        npm_cli = package / "cli.js"
        node = shutil.which("node")
        if client == "claude" and npm_cli.is_file() and node:
            return [node, str(npm_cli)]
        raise ValueError("Unsupported shell shim; use a native executable or export the prompt")
    return [executable]

def launch_plan(client, mode, request):
    directive = ("Use Claim in " + mode + " mode. First read " + str(SKILL / "SKILL.md")
                 + " and its selected references explicitly as UTF-8. Follow the mode's ownership and fresh web-search rules. "
                 "This is a new session; do not invent prior gate confirmations.\nUser request:\n" + request)
    command = client_command(client)
    if client == "codex":
        command += ["--search"]
    return command + ["--add-dir", str(SKILL), "--", directive]

def doctor(companion=None):
    info = {"claim_version": version(), "skill": str(SKILL),
            "clients": {name: shutil.which(name) for name in ("claude", "codex")},
            "lean_on_path": shutil.which("lean"), "lake_on_path": shutil.which("lake"),
            "network_and_auth": "NOT_TESTED"}
    candidate = companion
    info["companion_entry"] = str(candidate / "SKILL.md") if candidate and (candidate / "SKILL.md").is_file() else None
    info["companion_status"] = "ENTRY_PRESENT_NOT_EXECUTED" if info["companion_entry"] else "NOT_FOUND_OPTIONAL"
    return info

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version="Claim " + version())
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("doctor", help="Inspect local paths; no login or network requests")
    check.add_argument("--companion", type=Path, help="Optional user-selected local skill directory")
    export = commands.add_parser("prompt", help="Export UTF-8 instructions for another client")
    launch = commands.add_parser("run", help="Start the selected native interactive client")
    for cmd in (export, launch):
        cmd.add_argument("--mode", choices=MODES, default="coach")
        cmd.add_argument("--request", required=True)
    export.add_argument("--output", type=Path, help="Create a new file; never overwrite an existing file")
    launch.add_argument("--client", choices=("claude", "codex"), required=True)
    launch.add_argument("--dry-run", action="store_true", help="Print the argument list without starting a client")
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            print(json.dumps(doctor(args.companion), ensure_ascii=False, indent=2))
        elif args.command == "prompt":
            output = context(args.mode, args.request)
            if args.output:
                with args.output.open("x", encoding="utf-8", newline="\n") as file:
                    file.write(output)
                print("Created " + str(args.output))
            else:
                if hasattr(sys.stdout, "reconfigure"):
                    sys.stdout.reconfigure(encoding="utf-8")
                print(output, end="")
        else:
            command = launch_plan(args.client, args.mode, args.request)
            if args.dry_run:
                print(json.dumps(command, ensure_ascii=False, indent=2))
            else:
                return subprocess.run(command, shell=False).returncode
        return 0
    except (OSError, ValueError) as exc:
        print("Claim: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
