#!/usr/bin/env bash
# ==============================================================================
# Playwright Python Project Pre-setup Script (Bash / Linux / macOS / WSL)
# ==============================================================================

set -euo pipefail

echo ">>> [1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH. Please install Python 3.10+." >&2
    exit 1
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

$PYTHON_CMD --version

echo ""
echo ">>> [2/5] Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

echo ""
echo ">>> [3/5] Installing project dependencies from requirements.txt..."
$PYTHON_CMD -m pip install -r requirements.txt

echo ""
echo ">>> [4/5] Installing Playwright Chromium browser binaries..."
$PYTHON_CMD -m playwright install chromium

echo ""
echo ">>> [5/5] Creating project directory structure..."
mkdir -p tests/generated reports test-results

echo ""
echo ">>> [SUCCESS] Pre-setup completed successfully!"
echo "You can now run all tests in parallel with: pytest"
