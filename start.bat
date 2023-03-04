@echo off
REM Check if Docker is installed
docker -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed on this machine
    pause
    exit /b 1
)

REM Check if the Docker container is already built or running
docker ps -a | findstr /i "\<qbitpacker\>" >nul 2>&1
if %errorlevel% equ 0 (
    echo Docker container qbitpacker already exists or is running
    
    start "" http://localhost:5001
    timeout /t 5
    exit /b 1
)
mkdir -p mnt tmp downloads
REM Build the Docker image
docker build -t qbitpacker .

REM Start a Docker container based on the image
start docker run -d --restart unless-stopped --name qbitpacker -p 5001:5001 -p 8080:8080 qbitpacker

REM Wait for the Docker container to finish running

timeout /t 3
start "" http://localhost:5001
REM Exit the terminal
exit
