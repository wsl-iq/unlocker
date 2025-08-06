@echo off
:: +-------------------------------+
:: | #!/usr/bin/env bat            |
:: | -*- coding: utf-8 -*-         |
:: | Copyright (c) 2025            |
:: | Developer : Mohammed Al-Baqer |
:: +-------------------------------+
set "__Copyright__=Copyright (c) 2025"
set "__Developer__=Developer : Mohammed Al-Baqer"

echo %__Copyright__%
echo %__Developer__%

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Requires Administrator privileges Restarting as Admin...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

cd /d "%~dp0"

python "unlocker.py"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to execute unlocker.py
    pause
)
