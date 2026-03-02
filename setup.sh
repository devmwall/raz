#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This setup script is intended for Raspberry Pi OS/Linux." >&2
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "apt-get not found. This script requires a Debian-based system." >&2
  exit 1
fi

SUDO=""
if [[ "${EUID}" -ne 0 ]]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    echo "sudo not found and not running as root." >&2
    exit 1
  fi
fi

echo "Updating apt package index..."
$SUDO apt-get update

echo "Installing common Raspberry Pi Python/AI dependencies..."
$SUDO apt-get install -y \
  git \
  pciutils \
  python3 \
  python3-pip \
  python3-venv \
  python3-numpy \
  python3-opencv \
  python3-picamera2

if apt-cache show hailo-all >/dev/null 2>&1; then
  echo "Installing Hailo AI Kit bundle (hailo-all)..."
  $SUDO apt-get install -y hailo-all
elif apt-cache show hailort >/dev/null 2>&1; then
  echo "Installing Hailo runtime package (hailort)..."
  $SUDO apt-get install -y hailort
else
  cat <<'EOF'
Hailo packages are not available in current apt sources.
Install the Hailo AI Kit repository/packages from official Hailo docs,
then re-run this script to install them automatically.
EOF
fi

echo
echo "Setup complete. You can now run:"
echo "  bash ./ai-hat-test/run-ai-hat-test.sh --verbose"
