#!/usr/bin/env python3
"""Inspect or manage the official ChatGPT Chrome external-update entry on macOS."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

EXTENSION_ID = "hehggadaopoacecdllhhajmbjkdcmajg"
UPDATE_URL = "https://clients2.google.com/service/update2/crx"
EXPECTED = {"external_update_url": UPDATE_URL}


def default_root() -> Path:
    return Path.home() / "Library/Application Support/Google/Chrome"


def config_path(root: Path) -> Path:
    return root / "External Extensions" / f"{EXTENSION_ID}.json"


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"_error": str(exc)}


def status(path: Path) -> int:
    if not path.exists():
        print(json.dumps({"path": str(path), "present": False}, indent=2))
        return 0
    content = read_json(path)
    print(
        json.dumps(
            {
                "path": str(path),
                "present": True,
                "matches_expected": content == EXPECTED,
                "content": content,
            },
            indent=2,
        )
    )
    return 0


def install(path: Path, apply: bool) -> int:
    if path.exists():
        content = read_json(path)
        if content == EXPECTED:
            print(f"Already configured: {path}")
            return 0
        print(f"Refusing to overwrite unexpected content: {path}", file=sys.stderr)
        return 2
    if not apply:
        print(f"Dry run: would create {path}")
        print(json.dumps(EXPECTED, indent=2))
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(EXPECTED, indent=2) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=f".{EXTENSION_ID}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f"Created: {path}")
    return 0


def remove(path: Path, apply: bool) -> int:
    if not path.exists():
        print(f"Nothing to remove: {path}")
        return 0
    content = read_json(path)
    if content != EXPECTED:
        print(f"Refusing to remove unexpected content: {path}", file=sys.stderr)
        return 2
    if not apply:
        print(f"Dry run: would remove {path}")
        return 0
    path.unlink()
    print(f"Removed: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage the official ChatGPT Chrome external-update configuration."
    )
    parser.add_argument(
        "command", choices=("status", "install", "remove"), help="Operation to perform"
    )
    parser.add_argument(
        "--chrome-root",
        type=Path,
        default=default_root(),
        help="Chrome user-data root; primarily useful for testing",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually create or remove the file; otherwise changes are dry-run only",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    path = config_path(args.chrome_root.expanduser())
    if args.command == "status":
        return status(path)
    if args.command == "install":
        return install(path, args.apply)
    return remove(path, args.apply)


if __name__ == "__main__":
    raise SystemExit(main())

