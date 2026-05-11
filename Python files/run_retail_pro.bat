@echo off
echo ==========================================
echo STARTING RETAIL INTELLIGENCE PRO
echo ==========================================
echo [1/2] Checking dependencies...
pip install streamlit pandas plotly numpy scikit-learn
echo.
echo [2/2] Launching Dashboard...
streamlit run dashboard.py
pause
