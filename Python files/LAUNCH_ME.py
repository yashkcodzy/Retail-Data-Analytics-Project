import subprocess
import sys
import os

def run_app():
    print("==========================================")
    print("   RETAIL PRO DASHBOARD INITIALIZER")
    print("==========================================")
    
    # Install dependencies
    print("\n[1/2] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "plotly", "numpy"])
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        input("Press Enter to exit...")
        return

    # Run Streamlit
    print("\n[2/2] Launching Streamlit...")
    try:
        # Use sys.executable to run streamlit as a module
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except Exception as e:
        print(f"Error launching app: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    run_app()
