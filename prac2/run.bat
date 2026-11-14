@echo off

IF "%~1"=="" (
    SET CONFIG_PATH=config.xml
) ELSE (
    SET CONFIG_PATH=%~1
)

python -m src.main "%CONFIG_PATH%"

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error.
    pause
)