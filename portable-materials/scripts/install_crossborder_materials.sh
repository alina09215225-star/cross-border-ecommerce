#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_ARCHIVE="$ROOT_DIR/archives/crossborder-learning-distributor-skill-2026-07-12.tar.gz"
ROLE_ARCHIVE="$ROOT_DIR/archives/crossborder-knowledge-role-pack-lite-2026-07-12.tar.gz"

CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
CROSSBORDER_DIR="$HOME/Desktop/创收/跨境"

mkdir -p "$CODEX_SKILLS_DIR" "$CROSSBORDER_DIR"

if [[ ! -f "$SKILL_ARCHIVE" ]]; then
  echo "Missing skill archive: $SKILL_ARCHIVE" >&2
  exit 1
fi

if [[ ! -f "$ROLE_ARCHIVE" ]]; then
  echo "Missing role archive: $ROLE_ARCHIVE" >&2
  exit 1
fi

tar -xzf "$SKILL_ARCHIVE" -C "$CODEX_SKILLS_DIR"
tar -xzf "$ROLE_ARCHIVE" -C "$CROSSBORDER_DIR"

echo "Installed Codex skill to: $CODEX_SKILLS_DIR/crossborder-learning-distributor"
echo "Installed cross-border knowledge and role packs to: $CROSSBORDER_DIR"
echo "Next: ask Codex to use $crossborder-learning-distributor and read each role folder's _最新更新.md."
