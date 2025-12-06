# PowerShell script to run the CV-to-Job Matcher app
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

Write-Host "Starting Streamlit app..." -ForegroundColor Cyan
Write-Host "The app will open in your browser at http://localhost:8501" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m streamlit run app.py

