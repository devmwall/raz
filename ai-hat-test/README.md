# ai-hat-test

Quick hardware/software smoke test project for the Raspberry Pi AI M.2 HAT extension.

## What this checks

- Python runtime and platform details
- Optional AI stack imports (`hailo`, `picamera2`, `cv2`, `numpy`)
- Optional `lspci` probe for Hailo-like PCIe devices

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
