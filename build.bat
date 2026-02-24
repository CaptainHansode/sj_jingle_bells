@echo off
setlocal
cd /d %~dp0

echo [1/2] PyInstaller をインストール中...
.venv\Scripts\pip.exe install pyinstaller --quiet

echo [2/2] ビルド中...
.venv\Scripts\pyinstaller.exe ^
    --onefile ^
    --console ^
    --add-data "sound;sound" ^
    --name "jingle_bells" ^
    main.py

echo.
if %ERRORLEVEL% == 0 (
    echo ビルド成功！ dist\jingle_bells.exe が生成されました。
) else (
    echo ビルドに失敗しました。
)

pause
