# ==============================================================================
# Playwright Python Project Pre-setup Script (PowerShell / Windows)
# ==============================================================================

Write-Host ">>> [1/5] Checking Python installation..." -ForegroundColor Cyan
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.10+."
    exit 1
}
python --version

Write-Host "`n>>> [2/5] Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

Write-Host "`n>>> [3/5] Installing project dependencies from requirements.txt..." -ForegroundColor Cyan
python -m pip install -r requirements.txt

Write-Host "`n>>> [4/5] Installing Playwright Chromium browser binaries..." -ForegroundColor Cyan
python -m playwright install chromium

Write-Host "`n>>> [5/5] Creating project directory structure..." -ForegroundColor Cyan
$dirs = @("tests/generated", "reports", "test-results")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "Directory already exists: $dir" -ForegroundColor Gray
    }
}

Write-Host "`n>>> [SUCCESS] Pre-setup completed successfully!" -ForegroundColor Green
Write-Host "You can now run all tests in parallel with: pytest" -ForegroundColor Yellow
