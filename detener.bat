@echo off
setlocal
title Joyeria Matallana VIP - Detener

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\joyeria.ps1" -Action stop
if errorlevel 1 goto failed

echo.
echo Servicios de Joyeria Matallana VIP detenidos.
echo.
pause
exit /b 0

:failed
echo.
echo No se pudieron detener todos los servicios. Revisa los mensajes anteriores.
echo.
pause
exit /b 1
