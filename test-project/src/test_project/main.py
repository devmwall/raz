from __future__ import annotations

import argparse
import logging


LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Raspberry Pi Python starter app")
    parser.add_argument("--name", default="Raspberry Pi", help="Name to greet")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    return parser.parse_args()


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def run(name: str) -> int:
    LOGGER.info("Starting app")
    print(f"Hello, {name}!")
    LOGGER.info("Finished app")
    return 0


def main() -> int:
    args = parse_args()
    configure_logging(args.log_level)
    return run(args.name)


if __name__ == "__main__":
    raise SystemExit(main())
