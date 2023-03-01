@echo off
REM Check if Docker is installed
docker -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed on this machine
    timeout /T 5
    exit /b 1
)

REM Check if the Docker container is already running
docker inspect qbitpacker >nul 2>&1
if %errorlevel% equ 0 (
    echo Attempting to stop and delete qbitpacker container
    docker stop qbitpacker
    docker rm qbitpacker
    echo done
    timeout /T 5
    exit /b 0
)
