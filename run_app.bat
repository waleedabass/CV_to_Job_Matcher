@echo off
REM Batch script to run the CV-to-Job Matcher app
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting Streamlit app...
python -m streamlit run app.py

pause

