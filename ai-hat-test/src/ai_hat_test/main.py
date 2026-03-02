from __future__ import annotations

import argparse
import importlib
import platform
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleCheck:
    name: str
    ok: bool
    detail: str


MODULES_TO_CHECK = ("hailo", "picamera2", "cv2", "numpy")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Raspberry Pi AI M.2 HAT smoke test")
    parser.add_argument("--verbose", action="store_true", help="Print extra environment details")
    return parser.parse_args()


def check_module(name: str) -> ModuleCheck:
    try:
        module = importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001
        return ModuleCheck(name=name, ok=False, detail=f"missing ({exc.__class__.__name__})")

    version = getattr(module, "__version__", "unknown")
    return ModuleCheck(name=name, ok=True, detail=f"installed (version: {version})")


def detect_pcie_ai_device() -> str:
    try:
        result = subprocess.run(
            ["lspci"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return "lspci not available; skipped PCIe probe"

    if result.returncode != 0:
        return f"lspci returned non-zero exit code ({result.returncode})"

    lines = result.stdout.splitlines()
    hits = [line for line in lines if "hailo" in line.lower() or "co-processor" in line.lower()]
    if hits:
        return f"possible accelerator found: {hits[0]}"
    return "no obvious accelerator found in lspci output"


def main() -> int:
    args = parse_args()

    print("== Raspberry Pi AI HAT Test ==")
    print(f"Python: {platform.python_version()} ({sys.executable})")
    print(f"Platform: {platform.platform()}")

    checks = [check_module(name) for name in MODULES_TO_CHECK]
    print("\nModule checks:")
    for check in checks:
        status = "OK" if check.ok else "MISS"
        print(f"- {check.name:<10} {status} - {check.detail}")

    pcie_result = detect_pcie_ai_device()
    print("\nPCIe probe:")
    print(f"- {pcie_result}")

    if args.verbose:
        print("\nHints:")
        print("- Install missing Python packages in your project venv")
        print("- Confirm HAT drivers/runtime are installed per vendor docs")

    missing_count = sum(0 if check.ok else 1 for check in checks)
    if missing_count == len(checks):
        print("\nResult: no optional AI modules detected yet.")
        return 1

    print("\nResult: partial or full AI stack detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
