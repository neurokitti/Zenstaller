@echo off
:: Step 1: Clone the main repository
echo Cloning the main repository...
git clone https://github.com/neurokitti/desktop
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to clone the main repository.
    pause
    exit /b
)
echo Main repository cloned successfully.

:: Step 2: Navigate to the l10n folder
echo Navigating to the l10n folder...
cd desktop\l10n

:: Step 3: Clone the l10n-packs repository
echo Cloning the l10n-packs repository...
git clone https://github.com/neurokitti/l10n-packs
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to clone the l10n-packs repository.
    pause
    exit /b
)
echo l10n-packs repository cloned successfully.

:: Step 4: Move files from l10n-packs to the l10n folder
echo Moving files from l10n-packs into the l10n folder...
move l10n-packs\* .
rmdir /s /q l10n-packs
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to move files from l10n-packs.
    pause
    exit /b
)
echo Files moved successfully.

:: Step 5: Return to the desktop folder and run npm commands
cd ..
echo Running npm commands...
npm i
npm run init
npm run bootstrap

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to complete npm setup.
    pause
    exit /b
)
echo npm setup completed successfully.

:: Step 6: Download the Zen_install.py Python script from GitHub
cd ..
echo Downloading the Zen_install.py Python script from GitHub...
curl -L -o Zen_install.py https://github.com/neurokitti/Zenstaller/raw/main/Zen_install.py
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to download Zen_install.py.
    pause
    exit /b
)
echo Zen_install.py downloaded successfully.

:: Step 7: Run the Python script to update the mozconfig file
echo Running the Python script...
python Zen_install.py
if %ERRORLEVEL% neq 0 (
    echo Error: Python script execution failed.
    pause
    exit /b
)


echo Python script executed successfully.
cd desktop
:: Script completed
echo running npm build.
npm run build
