from __future__ import annotations

import argparse
import shutil
import subprocess
import time
from pathlib import Path

from picamera2 import Picamera2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Turn on Pi camera and capture one frame")
    parser.add_argument(
        "--output",
        default="camera-test.jpg",
        help="Output image path (default: camera-test.jpg)",
    )
    parser.add_argument(
        "--warmup-seconds",
        type=float,
        default=2.0,
        help="Seconds to keep camera running before capture",
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Camera index to open (default: 0)",
    )
    parser.add_argument(
        "--fallback-rpicam-still",
        action="store_true",
        help="Fallback to rpicam-still if Picamera2 capture fails",
    )
    return parser.parse_args()


def capture_with_rpicam_still(output_path: Path, warmup_seconds: float) -> int:
    cmd = [
        "rpicam-still",
        "-n",
        "-t",
        str(int(max(0.0, warmup_seconds) * 1000)),
        "-o",
        str(output_path),
    ]
    print("Running fallback:", " ".join(cmd))
    return subprocess.run(cmd, check=False).returncode


def main() -> int:
    args = parse_args()
    output_path = Path(args.output).expanduser().resolve()

    camera = Picamera2(args.camera_index)
    config = camera.create_still_configuration(main={"size": (2304, 1296)})
    camera.configure(config)

    try:
        print("Starting camera...")
        camera.start()
        time.sleep(max(0.0, args.warmup_seconds))

        print(f"Capturing image to: {output_path}")
        camera.capture_file(str(output_path))
    except Exception as exc:  # noqa: BLE001
        print(f"Picamera2 capture failed: {exc}")
        if args.fallback_rpicam_still and shutil.which("rpicam-still"):
            return_code = capture_with_rpicam_still(output_path, args.warmup_seconds)
            if return_code == 0:
                print("Camera test complete via rpicam-still fallback.")
                return 0
        return 1
    finally:
        camera.stop()

    print("Camera test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
