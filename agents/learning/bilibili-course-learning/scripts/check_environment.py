#!/usr/bin/env python3
"""
Check whether the Bilibili course learning runtime is ready.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
MODEL_DIRS = [
    SKILL_DIR / "assets" / "models",
    Path.home() / ".cache" / "bilibili-course-learning" / "models",
]
MODEL_NAMES = ["ggml-small.bin", "ggml-base.bin"]


def command_version(command: str, args: list[str]) -> str:
    binary = shutil.which(command)
    if not binary:
        return "missing"
    try:
        result = subprocess.run(
            [binary, *args],
            check=False,
            text=True,
            capture_output=True,
            timeout=20,
        )
    except Exception as exc:
        return f"found, version check failed: {exc}"
    first_line = (result.stdout or result.stderr).splitlines()
    return first_line[0] if first_line else "found"


def find_models() -> list[Path]:
    found: list[Path] = []
    for directory in MODEL_DIRS:
        for name in MODEL_NAMES:
            path = directory / name
            if path.exists():
                found.append(path)
    return found


def main() -> None:
    checks = {
        "yt-dlp": command_version("yt-dlp", ["--version"]),
        "ffmpeg": command_version("ffmpeg", ["-version"]),
        "whisper-cli": command_version("whisper-cli", ["--help"]),
    }

    print("Bilibili course learning environment")
    print("")
    ok = True
    for name, value in checks.items():
        status = "OK" if value != "missing" else "MISSING"
        if value == "missing":
            ok = False
        print(f"- {name}: {status} ({value})")

    models = find_models()
    if models:
        print("- whisper model: OK")
        for model in models:
            print(f"  {model}")
    else:
        ok = False
        print("- whisper model: MISSING")
        print("  Run: ./scripts/download_whisper_model.sh small")

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
