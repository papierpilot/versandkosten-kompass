@echo off
setlocal

title Versandkosten-Kompass v0.5.0-tes

cd /d "%~dp0"

call .venv\Scripts\activate.bat

py -m streamlit run versand_app.py --server.port 8506

pause