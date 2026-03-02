# test-project

Starter Python template for Raspberry Pi projects.

## Features

- `src/` layout with a clean package structure
- CLI entry point (`test-project`)
- Logging configured for easy debugging on-device
- `pytest` test setup
- `ruff` and `mypy` dev tooling

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
test-project --name Pi
pytest
```

## Project layout

```text
test-project/
  src/test_project/
    __init__.py
    main.py
  tests/
    test_smoke.py
  pyproject.toml
```

## Raspberry Pi notes

- On Raspberry Pi OS, install Python tooling first:
  `sudo apt update && sudo apt install -y python3-venv python3-pip`
- Add hardware libs later as needed (for example `gpiozero`, `RPi.GPIO`).
