@echo off
pushd %~dp0
echo ==========================================
echo RETAIL INTELLIGENCE PRO: FULL-STACK SAAS
echo ==========================================

echo [1/3] Installing Backend Dependencies...
pip install -r requirements.txt

echo [2/3] Starting FastAPI Backend...
start cmd /k "python backend/main.py"

echo [3/3] Starting React Frontend...
cd frontend
echo (Make sure you have Node.js installed)
npm install && npm run dev

pause
