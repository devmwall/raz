# raz workspace

This repository is a top-level workspace for multiple projects.

## Projects

- `test-project/` - Python Raspberry Pi starter template
- `ai-hat-test/` - Raspberry Pi AI M.2 HAT smoke test project

## How to use this workspace

1. Enter the project you want to work on.
2. Follow that project's README for setup and run commands.

For Raspberry Pi dependency bootstrap from repo root:

```bash
chmod +x setup.sh
bash ./setup.sh
```

Example:

```bash
cd test-project
```

For AI HAT testing:

```bash
cd ai-hat-test
bash ./run-ai-hat-test.sh
```

## test-project quick commands

From repo root (`raz`):

```bash
bash ./test-project/run-test-project.sh --name Pi
```

From inside `test-project/`:

```bash
bash ./run-test-project.sh --name Pi
```

Optional (Linux) to run directly:

```bash
chmod +x run-test-project.sh
./run-test-project.sh --name Pi
```

If you see line-ending errors on Raspberry Pi, normalize once:

```bash
sed -i 's/\r$//' run-test-project.sh
```
