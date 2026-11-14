@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
title AllayOps Fabric Server

REM ============================================================================
REM AllayOps Portable Enterprise Startup Script
REM - Works on any Windows host (auto-discovers Java & scales heap to host RAM)
REM - Supports optional overrides via .env (MC_JAVA_XMS, MC_JAVA_XMX, etc.)
REM ============================================================================

REM 1. Load optional overrides from .env (ignores comments & blank lines)
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        set "KEY=%%A"
        if not "!KEY!"=="" if not "!KEY:~0,1!"=="#" (
            set "!KEY!=%%B"
        )
    )
)

REM 2. Discover Java executable (MC_JAVA_EXE -> JAVA_HOME -> PATH -> Adoptium/Java)
set "JAVA_EXE="
if defined MC_JAVA_EXE if exist "%MC_JAVA_EXE%" set "JAVA_EXE=%MC_JAVA_EXE%"
if not defined JAVA_EXE if defined JAVA_HOME if exist "%JAVA_HOME%\bin\java.exe" set "JAVA_EXE=%JAVA_HOME%\bin\java.exe"
if not defined JAVA_EXE (
    for /f "delims=" %%J in ('where java 2^>nul') do (
        if not defined JAVA_EXE set "JAVA_EXE=%%J"
    )
)
if not defined JAVA_EXE (
    for %%R in ("C:\Program Files\Eclipse Adoptium" "C:\Program Files\Java" "C:\Program Files\Microsoft") do (
        if exist "%%~R" (
            for /d %%D in ("%%~R\jdk-25*" "%%~R\jdk-21*" "%%~R\jdk-*") do (
                if not defined JAVA_EXE if exist "%%~D\bin\java.exe" set "JAVA_EXE=%%~D\bin\java.exe"
            )
        )
    )
)
if not defined JAVA_EXE (
    echo [ERROR] No Java runtime found. Install Eclipse Adoptium JDK 25 or set JAVA_HOME / MC_JAVA_EXE in .env.
    pause
    exit /b 1
)

REM 3. Auto-scale Heap to Host RAM if not set in .env
if not defined MC_JAVA_XMS set "MC_JAVA_XMS="
if not defined MC_JAVA_XMX set "MC_JAVA_XMX="
if not defined MC_JAVA_XMX (
    for /f "delims=" %%M in ('powershell -NoProfile -Command "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)" 2^>nul') do set "HOST_RAM_GB=%%M"
    if not defined HOST_RAM_GB set "HOST_RAM_GB=16"
    if !HOST_RAM_GB! GEQ 31 (
        set "MC_JAVA_XMS=4G"
        set "MC_JAVA_XMX=8G"
    ) else if !HOST_RAM_GB! GEQ 15 (
        set "MC_JAVA_XMS=2G"
        set "MC_JAVA_XMX=4G"
    ) else (
        set "MC_JAVA_XMS=1G"
        set "MC_JAVA_XMX=2G"
    )
)
if not defined MC_JAVA_XMS set "MC_JAVA_XMS=2G"

REM 4. Probe JDK capabilities (ZGC + StringDeduplication + CompactObjectHeaders on JDK 24/25+)
set "JVM_FLAGS=-Xms%MC_JAVA_XMS% -Xmx%MC_JAVA_XMX% -XX:+UseZGC -XX:+UseStringDeduplication -XX:+ExitOnOutOfMemoryError -Dfile.encoding=UTF-8"
"%JAVA_EXE%" -XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders -version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "JVM_FLAGS=%JVM_FLAGS% -XX:+UnlockExperimentalVMOptions -XX:+UseCompactObjectHeaders"
)
if /I "%MC_PRETOUCH%"=="true" set "JVM_FLAGS=%JVM_FLAGS% -XX:+AlwaysPreTouch"
if defined MC_EXTRA_JVM_ARGS set "JVM_FLAGS=%JVM_FLAGS% %MC_EXTRA_JVM_ARGS%"

REM 5. Pre-flight config & EULA checks
if not exist "server.properties" if exist "server.properties.example" (
    echo [INFO] server.properties not found. Copying from server.properties.example...
    copy /y "server.properties.example" "server.properties" >nul
)
if not exist "eula.txt" (
    echo [WARN] eula.txt not found. First launch will generate eula.txt — set eula=true to accept.
) else (
    findstr /I /C:"eula=true" "eula.txt" >nul || (
        echo [WARN] eula=true is not set in eula.txt. Server may exit until EULA is accepted.
    )
)

REM 6. Locate Fabric launcher JAR
set "SERVER_JAR="
for %%F in (fabric-server*.jar) do (
    if not defined SERVER_JAR set "SERVER_JAR=%%F"
)
if not defined SERVER_JAR (
    echo [ERROR] No fabric-server*.jar found in %CD%
    pause
    exit /b 1
)

:launch
echo ============================================================================
echo [AllayOps] Starting %SERVER_JAR%
echo [AllayOps] Java : %JAVA_EXE%
echo [AllayOps] Flags: %JVM_FLAGS%
echo ============================================================================
"%JAVA_EXE%" %JVM_FLAGS% -jar "%SERVER_JAR%" nogui
set "EXIT_CODE=%ERRORLEVEL%"
echo [AllayOps] Server exited with code %EXIT_CODE%.

if /I "%MC_AUTO_RESTART%"=="true" if not "%EXIT_CODE%"=="0" (
    echo [AllayOps] Crash detected. Restarting in 5 seconds (Press Ctrl+C to cancel)...
    timeout /t 5 /nobreak >nul
    goto :launch
)

pause
exit /b %EXIT_CODE%
