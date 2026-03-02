#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_SRC="$SCRIPT_DIR/src"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python3 or python is required but was not found in PATH." >&2
  exit 127
fi

PYTHONPATH="$PROJECT_SRC${PYTHONPATH:+:$PYTHONPATH}" "$PYTHON_BIN" -m ai_hat_test.camera_test "$@"
