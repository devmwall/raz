#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_MODEL_PATH="$SCRIPT_DIR/models/cas_vit_s.hef"

MODEL_PATH="${1:-$DEFAULT_MODEL_PATH}"

if [[ ! -f "$MODEL_PATH" ]]; then
  echo "Model file not found: $MODEL_PATH" >&2
  exit 2
fi

if [[ "$MODEL_PATH" == *.onnx ]]; then
  echo "Model is ONNX: $MODEL_PATH"
  echo "Hailo runtime executes HEF files, not ONNX directly." >&2
  echo "Compile this ONNX to a .hef with Hailo tooling, then run:" >&2
  echo "  $0 /path/to/model.hef" >&2
  exit 2
fi

HEF_PATH="$MODEL_PATH"

if ! command -v hailortcli >/dev/null 2>&1; then
  echo "hailortcli not found in PATH." >&2
  exit 127
fi

echo "== Hailo Model Smoke Test =="
hailortcli --version
echo
echo "Parsing model: $HEF_PATH"
hailortcli parse-hef "$HEF_PATH"
echo
echo "Trying runtime execution..."

if hailortcli benchmark "$HEF_PATH"; then
  echo
  echo "Model execution succeeded via: hailortcli benchmark"
  exit 0
fi

if hailortcli run "$HEF_PATH"; then
  echo
  echo "Model execution succeeded via: hailortcli run"
  exit 0
fi

echo
echo "Could not run model with default commands." >&2
echo "Check available commands/options with: hailortcli --help" >&2
exit 1
