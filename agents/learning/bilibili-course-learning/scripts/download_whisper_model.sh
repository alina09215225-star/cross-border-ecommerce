#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-small}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_DIR="${SCRIPT_DIR}/../assets/models"
mkdir -p "${MODEL_DIR}"

case "${MODEL}" in
  small)
    FILE="ggml-small.bin"
    URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin"
    ;;
  base)
    FILE="ggml-base.bin"
    URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin"
    ;;
  *)
    echo "Usage: $0 [small|base]" >&2
    exit 2
    ;;
esac

OUT="${MODEL_DIR}/${FILE}"
if [[ -f "${OUT}" ]]; then
  echo "Model already exists: ${OUT}"
  exit 0
fi

echo "Downloading ${FILE}..."
curl -L -C - "${URL}" -o "${OUT}"
echo "Saved model: ${OUT}"
