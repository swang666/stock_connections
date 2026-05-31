@echo off
REM Double-click to launch Claude Code in the stock knowledge base.
REM Right-click -> "Create shortcut" and drag to the desktop or pin to taskbar.
cd /d "%~dp0"
echo Launching Claude Code in: %CD%
echo (Reads CLAUDE.md automatically. Type your question.)
echo.
claude
