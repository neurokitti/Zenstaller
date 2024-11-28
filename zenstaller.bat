@echo off
:: Step 1: Download the Zen_install.py Python script from GitHub
echo Downloading the Zen_install.py Python script from GitHub...
curl -L -o Zen_install.py https://github.com/neurokitti/Zenstaller/raw/main/Zen_install.py

:: Check if the download was successful
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to download Zen_install.py.
    exit /b
)
echo Zen_install.py downloaded successfully.
pause
cd
pause
:: Step 2: Run the Python script to handle the rest of the installation
echo Running the Python script...
python Zen_install.py

:: Check if the Python script ran successfully
if %ERRORLEVEL% neq 0 (
    echo Error: Python script execution failed.
    exit /b
)

echo Python script executed successfully.
:: Script completed
pause
