#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required on macOS. Install Homebrew first: https://brew.sh/" >&2
  exit 1
fi

brew install yt-dlp ffmpeg whisper-cpp
echo "Runtime installed. Next run: ./scripts/download_whisper_model.sh small"
