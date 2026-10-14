@echo off
chcp 65001 >nul
echo === Встановлення PyInstaller ===
python -m pip install --upgrade pyinstaller || goto :error
echo === Збірка PocketTools.exe ===
python -m PyInstaller --onefile --windowed --name PocketTools main.py || goto :error
copy /Y dist\PocketTools.exe PocketTools.exe >nul
echo.
echo Готово! PocketTools.exe лежить поруч із main.py
pause
exit /b 0
:error
echo.
echo Помилка збірки. Перевірте, що встановлено Python (python --version).
pause
exit /b 1
