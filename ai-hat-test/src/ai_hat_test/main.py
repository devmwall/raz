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


@dataclass(frozen=True)
class CommandCheck:
    name: str
    ok: bool
    detail: str


MODULES_TO_CHECK = ("hailo_platform", "hailo", "picamera2", "cv2", "numpy")


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


def check_command(name: str, args: list[str]) -> CommandCheck:
    try:
        result = subprocess.run(
            [name, *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return CommandCheck(name=name, ok=False, detail="missing from PATH")

    if result.returncode == 0:
        first_line = (result.stdout.strip() or result.stderr.strip() or "ok").splitlines()[0]
        return CommandCheck(name=name, ok=True, detail=first_line)

    first_error = (result.stderr.strip() or result.stdout.strip() or "failed").splitlines()[0]
    return CommandCheck(name=name, ok=False, detail=f"exit {result.returncode}: {first_error}")


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

    command_checks = [
        check_command("hailortcli", ["--version"]),
        check_command("hailortcli", ["fw-control", "identify"]),
    ]
    print("\nHailo runtime checks:")
    for check in command_checks:
        status = "OK" if check.ok else "MISS"
        print(f"- {check.name:<10} {status} - {check.detail}")

    if args.verbose:
        print("\nHints:")
        print("- Hailo AI Kit usually needs system packages plus Python bindings")
        print("- If hailortcli is missing, install HailoRT from vendor instructions")
        print("- If fw-control identify fails, check PCIe seating and power")

    modules_ok = any(check.ok for check in checks)
    commands_ok = all(check.ok for check in command_checks)
    if not modules_ok and not commands_ok:
        print("\nResult: Hailo stack not detected yet.")
        return 1

    if modules_ok and commands_ok:
        print("\nResult: Hailo AI Kit looks healthy.")
        return 0

    print("\nResult: partial Hailo setup detected; some pieces still missing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
