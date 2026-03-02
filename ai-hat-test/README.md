# ai-hat-test

Quick hardware/software smoke test project for the Raspberry Pi Hailo AI Kit (AI M.2 HAT).

## What this checks

- Python runtime and platform details
- Optional AI stack imports (`hailo_platform`, `hailo`, `picamera2`, `cv2`, `numpy`)
- `hailortcli --version` and `hailortcli fw-control identify`
- `lspci` probe for Hailo-like PCIe devices

## Run

From inside this folder:

```bash
bash ./run-ai-hat-test.sh
```

From repo root:

```bash
bash ./ai-hat-test/run-ai-hat-test.sh
```

## Install optional modules

The script works without these, but installing them gives a more complete check.

```bash
python3 -m pip install -e .
python3 -m pip install numpy opencv-python
```

`hailo` and `picamera2` are often installed from Raspberry Pi/Hailo packages rather than PyPI depending on your image.

## Hailo AI Kit notes

- A healthy setup usually shows both `hailortcli` checks as OK and at least one Hailo Python import as OK.
- If `hailortcli` is missing, install the Hailo runtime/tooling from the official AI Kit setup flow.
- If `fw-control identify` fails, reseat the M.2 card and recheck power/PCIe enablement.
