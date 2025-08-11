
@echo off
REM JARVIS AI Assistant Deployment Script for Windows

echo 🤖 Starting JARVIS AI Assistant deployment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [SUCCESS] Python found
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip not found. Please install pip.
    pause
    exit /b 1
)

echo [SUCCESS] pip found
echo.

REM Create virtual environment
echo [INFO] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [INFO] Installing Python requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [SUCCESS] Requirements installed
echo.

REM Create directory structure
echo [INFO] Creating directory structure...
if not exist config mkdir config
if not exist data mkdir data
if not exist logs mkdir logs
if not exist assets mkdir assets
if not exist assets\audio mkdir assets\audio
if not exist assets\images mkdir assets\images
if not exist modules mkdir modules
echo [SUCCESS] Directory structure created
echo.

REM Setup configuration files
echo [INFO] Setting up configuration files...

REM Create default user preferences
if not exist config\user_preferences.json (
    echo {> config\user_preferences.json
    echo     "voice_enabled": true,>> config\user_preferences.json
    echo     "wake_word": "jarvis",>> config\user_preferences.json
    echo     "confidence_threshold": 0.7,>> config\user_preferences.json
    echo     "response_speed": 1.0,>> config\user_preferences.json
    echo     "theme": "dark",>> config\user_preferences.json
    echo     "auto_save_conversations": true,>> config\user_preferences.json
    echo     "max_conversation_history": 100>> config\user_preferences.json
    echo }>> config\user_preferences.json
    echo [SUCCESS] Default user preferences created
)

REM Create Streamlit config
if not exist .streamlit mkdir .streamlit
if not exist .streamlit\config.toml (
    echo [global]> .streamlit\config.toml
    echo developmentMode = false>> .streamlit\config.toml
    echo.>> .streamlit\config.toml
    echo [server]>> .streamlit\config.toml
    echo headless = true>> .streamlit\config.toml
    echo enableCORS = true>> .streamlit\config.toml
    echo port = 8501>> .streamlit\config.toml
    echo.>> .streamlit\config.toml
    echo [theme]>> .streamlit\config.toml
    echo primaryColor = "#00d4ff">> .streamlit\config.toml
    echo backgroundColor = "#0e1117">> .streamlit\config.toml
    echo secondaryBackgroundColor = "#262730">> .streamlit\config.toml
    echo textColor = "#fafafa">> .streamlit\config.toml
    echo font = "sans serif">> .streamlit\config.toml
    echo.>> .streamlit\config.toml
    echo [browser]>> .streamlit\config.toml
    echo gatherUsageStats = false>> .streamlit\config.toml
    echo [SUCCESS] Streamlit config created
)

echo.
echo [SUCCESS] Deployment completed successfully!
echo.
echo To start JARVIS manually, run:
echo   venv\Scripts\activate.bat
echo   streamlit run streamlit_app.py
echo.
echo Access the application at: http://localhost:8501
echo.

set /p start="Do you want to start JARVIS now? (y/n): "
if /i "%start%"=="y" (
    echo [INFO] Starting JARVIS AI Assistant...
    streamlit run streamlit_app.py
)

pause
