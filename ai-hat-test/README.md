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

To prove a model can execute on-device (with a HEF file):

```bash
bash ./run-model-smoke.sh /path/to/model.hef
```

To test camera bring-up (turn camera on and capture one frame):

```bash
bash ./run-camera-test.sh --output ./camera-test.jpg
```

If Picamera2 is unstable on your setup, enable CLI fallback:

```bash
bash ./run-camera-test.sh --output ./camera-test.jpg --fallback-rpicam-still
```

Default model path in script points to:

`ai-hat-test/models/repghost_1_0x.hef`

You can still pass another model path explicitly if needed.

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
- You can run models with `hailortcli` even when Python modules (`hailo`, `hailo_platform`) are not installed.
