#!/usr/bin/env python3
"""
Fetch study material from a Bilibili video URL using subtitles first,
then fall back to local audio transcription with whisper.cpp.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from normalize_bilibili_subtitles import detect_and_parse  # noqa: E402
from prepare_bilibili_study_material import build_markdown, chunk_text  # noqa: E402


MANUAL_LANG_PREFERENCE = [
    "zh-Hans",
    "zh-CN",
    "zh",
    "cmn-Hans",
    "zh-Hant",
    "zh-TW",
    "en",
]

AUTO_LANG_PREFERENCE = [
    "ai-zh",
    "zh-Hans",
    "zh-CN",
    "zh",
    "ai-en",
    "en",
]

SUBTITLE_EXTENSIONS = {".srt", ".vtt", ".json", ".json3", ".ass", ".srv1", ".srv2", ".srv3"}
AUDIO_EXTENSIONS = {".m4a", ".mp3", ".aac", ".webm", ".ogg", ".wav", ".flac"}
DEFAULT_MODEL_CACHE_DIR = Path.home() / ".cache" / "bilibili-course-learning" / "models"
DEFAULT_MODEL_LOCAL_DIR = SCRIPT_DIR.parent / "assets" / "models"
DEFAULT_MODEL_CANDIDATES = [
    "ggml-small.bin",
    "ggml-base.bin",
]
DEFAULT_MODEL_URLS = {
    "ggml-small.bin": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin",
    "ggml-base.bin": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin",
}


def run_command(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        message = f"Command failed: {' '.join(cmd)}"
        if detail:
            message += f"\n\n{detail}"
        raise SystemExit(message) from exc


def require_yt_dlp() -> str:
    binary = shutil.which("yt-dlp")
    if not binary:
        raise SystemExit("yt-dlp is not installed. Install it first, then retry.")
    return binary


def require_binary(name: str, install_hint: str) -> str:
    binary = shutil.which(name)
    if not binary:
        raise SystemExit(f"{name} is not installed. {install_hint}")
    return binary


def fetch_info(
    yt_dlp_bin: str,
    url: str,
    cookies_from_browser: str | None,
    cookies_file: str | None,
) -> dict:
    cmd = [yt_dlp_bin, "--dump-single-json", "--skip-download", "--no-playlist", "--no-warnings", url]
    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    if cookies_file:
        cmd.extend(["--cookies", cookies_file])
    result = run_command(cmd)
    return json.loads(result.stdout)


def pick_language(info: dict) -> tuple[str, str] | None:
    subtitles = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}

    for lang in MANUAL_LANG_PREFERENCE:
        if subtitles.get(lang):
            return "manual", lang
    for lang in subtitles:
        return "manual", lang

    for lang in AUTO_LANG_PREFERENCE:
        if automatic.get(lang):
            return "auto", lang
    for lang in automatic:
        return "auto", lang

    return None


def download_subtitles(
    yt_dlp_bin: str,
    url: str,
    lang: str,
    destination: Path,
    cookies_from_browser: str | None,
    cookies_file: str | None,
) -> None:
    cmd = [
        yt_dlp_bin,
        "--no-playlist",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        lang,
        "--output",
        str(destination / "%(title)s [%(id)s].%(ext)s"),
        url,
    ]
    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    if cookies_file:
        cmd.extend(["--cookies", cookies_file])
    run_command(cmd)


def find_subtitle_file(directory: Path) -> Path:
    candidates = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUBTITLE_EXTENSIONS
    ]
    if not candidates:
        raise SystemExit("yt-dlp ran, but no subtitle file was produced.")
    candidates.sort(key=lambda path: (path.suffix.lower() != ".json", path.name))
    return candidates[0]


def find_audio_file(directory: Path) -> Path:
    candidates = [
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS
    ]
    if not candidates:
        raise SystemExit("yt-dlp ran, but no audio file was produced for transcription.")
    candidates.sort()
    return candidates[0]


def download_audio(
    yt_dlp_bin: str,
    url: str,
    destination: Path,
    cookies_from_browser: str | None,
    cookies_file: str | None,
) -> Path:
    cmd = [
        yt_dlp_bin,
        "--no-playlist",
        "-f",
        "ba/b",
        "--output",
        str(destination / "%(title)s [%(id)s].%(ext)s"),
        url,
    ]
    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    if cookies_file:
        cmd.extend(["--cookies", cookies_file])
    run_command(cmd)
    return find_audio_file(destination)


def convert_audio_to_wav(ffmpeg_bin: str, audio_path: Path, wav_path: Path) -> None:
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i",
        str(audio_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(wav_path),
    ]
    run_command(cmd)


def resolve_model_path(custom_path: str | None) -> Path:
    explicit_candidates = [custom_path, os.environ.get("BILIBILI_WHISPER_MODEL")]
    for candidate in explicit_candidates:
        if candidate:
            path = Path(candidate).expanduser()
            if path.exists():
                return path

    for model_name in DEFAULT_MODEL_CANDIDATES:
        for directory in (DEFAULT_MODEL_LOCAL_DIR, DEFAULT_MODEL_CACHE_DIR):
            path = directory / model_name
            if path.exists():
                return path
    raise SystemExit(
        "No whisper.cpp model file found.\n"
        f"Expected default directories: {DEFAULT_MODEL_LOCAL_DIR} or {DEFAULT_MODEL_CACHE_DIR}\n"
        "Recommended model downloads:\n"
        + "\n".join(f"- {name}: {url}" for name, url in DEFAULT_MODEL_URLS.items())
        + "\n"
        "Or pass --whisper-model /path/to/ggml-model.bin."
    )


def transcribe_with_whisper_cpp(
    whisper_cli_bin: str,
    model_path: Path,
    wav_path: Path,
    output_base: Path,
) -> str:
    cmd = [
        whisper_cli_bin,
        "-m",
        str(model_path),
        "-f",
        str(wav_path),
        "-l",
        "auto",
        "-otxt",
        "-of",
        str(output_base),
        "-np",
    ]
    run_command(cmd)
    text_path = output_base.with_suffix(".txt")
    if not text_path.exists():
        raise SystemExit("whisper.cpp finished, but no transcript text file was created.")
    return text_path.read_text(encoding="utf-8").strip()


def safe_name(name: str) -> str:
    keep = "".join(ch if ch.isalnum() or ch in " -_()" else " " for ch in name)
    return " ".join(keep.split()).strip() or "bilibili-course"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch Bilibili study material from subtitles or local transcription."
    )
    parser.add_argument("url", help="Bilibili video URL")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory for transcript and study markdown",
    )
    parser.add_argument(
        "--cookies-from-browser",
        help="Pass through to yt-dlp, e.g. chrome, safari, edge",
    )
    parser.add_argument(
        "--cookies",
        help="Path to a cookies.txt file exported from your browser",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1800,
        help="Approximate character limit per study chunk",
    )
    parser.add_argument(
        "--goal",
        default="理解课程核心内容，并整理成可复习、可应用的材料。",
        help="Learning goal written into the study markdown",
    )
    parser.add_argument(
        "--whisper-model",
        help="Path to a local whisper.cpp GGML model file for audio transcription fallback",
    )
    args = parser.parse_args()

    yt_dlp_bin = require_yt_dlp()
    info = fetch_info(yt_dlp_bin, args.url, args.cookies_from_browser, args.cookies)
    subtitle_choice = pick_language(info)

    title = info.get("title") or info.get("id") or "Bilibili 课程"
    base_name = safe_name(title)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    transcript_source = ""
    language = ""

    with tempfile.TemporaryDirectory(prefix="bili-course-") as tmp:
        tmpdir = Path(tmp)
        if subtitle_choice is not None:
            subtitle_mode, lang = subtitle_choice
            download_subtitles(
                yt_dlp_bin,
                args.url,
                lang,
                tmpdir,
                args.cookies_from_browser,
                args.cookies,
            )
            subtitle_file = find_subtitle_file(tmpdir)
            transcript = detect_and_parse(subtitle_file, keep_timestamps=False)
            transcript_source = f"subtitles:{subtitle_mode}"
            language = lang
        else:
            ffmpeg_bin = require_binary("ffmpeg", "Install it first, then retry.")
            whisper_cli_bin = require_binary("whisper-cli", "Install whisper-cpp first, then retry.")
            model_path = resolve_model_path(args.whisper_model)
            audio_path = download_audio(
                yt_dlp_bin,
                args.url,
                tmpdir,
                args.cookies_from_browser,
                args.cookies,
            )
            wav_path = tmpdir / "audio.wav"
            convert_audio_to_wav(ffmpeg_bin, audio_path, wav_path)
            transcript = transcribe_with_whisper_cpp(
                whisper_cli_bin,
                model_path,
                wav_path,
                tmpdir / "transcript",
            )
            transcript_source = "whisper-cpp"
            language = "auto"

    transcript_path = output_dir / f"{base_name}.transcript.txt"
    transcript_path.write_text(transcript + "\n", encoding="utf-8")

    chunks = chunk_text(transcript, args.chunk_size)
    study_markdown = build_markdown(
        title=title,
        goal=args.goal,
        source=args.url,
        chunks=chunks,
    )
    study_path = output_dir / f"{base_name}.study.md"
    study_path.write_text(study_markdown, encoding="utf-8")

    summary = {
        "title": title,
        "transcript_source": transcript_source,
        "language": language,
        "transcript_path": str(transcript_path),
        "study_path": str(study_path),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
