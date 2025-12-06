# PowerShell script to install packages in virtual environment
# Run this script: .\install_packages.ps1

Write-Host "Installing packages in virtual environment..." -ForegroundColor Green

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Upgrade pip first
python -m pip install --upgrade pip --no-cache-dir

# Install packages one by one to avoid file lock issues
Write-Host "Installing streamlit..." -ForegroundColor Yellow
python -m pip install streamlit --no-cache-dir

Write-Host "Installing PyPDF2..." -ForegroundColor Yellow
python -m pip install PyPDF2 --no-cache-dir

Write-Host "Installing python-docx..." -ForegroundColor Yellow
python -m pip install python-docx --no-cache-dir

Write-Host "Installing reportlab..." -ForegroundColor Yellow
python -m pip install reportlab --no-cache-dir

Write-Host "Installing numpy..." -ForegroundColor Yellow
python -m pip install numpy --no-cache-dir

Write-Host "Installing pandas..." -ForegroundColor Yellow
python -m pip install pandas --no-cache-dir

Write-Host "`nInstallation complete! Verifying..." -ForegroundColor Green
python -m pip list | Select-String -Pattern "streamlit|PyPDF2|docx|reportlab|numpy|pandas"

Write-Host "`nTo run the app, use: python -m streamlit run app.py" -ForegroundColor Cyan

