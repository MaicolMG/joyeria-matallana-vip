@echo off
setlocal
title Joyeria Matallana VIP - Iniciar

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\joyeria.ps1" -Action start
if errorlevel 1 goto failed

echo.
echo Joyeria Matallana VIP esta lista.
echo Tienda: http://localhost:8501
echo API:    http://localhost:3000
echo.
pause
exit /b 0

:failed
echo.
echo No se pudo iniciar la aplicacion. Revisa los mensajes anteriores.
echo.
pause
exit /b 1
