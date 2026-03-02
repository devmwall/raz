from __future__ import annotations

import argparse
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output).expanduser().resolve()

    camera = Picamera2()
    config = camera.create_still_configuration()
    camera.configure(config)

    print("Starting camera...")
    camera.start()
    time.sleep(max(0.0, args.warmup_seconds))

    print(f"Capturing image to: {output_path}")
    camera.capture_file(str(output_path))
    camera.stop()

    print("Camera test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
