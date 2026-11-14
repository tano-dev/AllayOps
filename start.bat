@echo off
cd /d "%~dp0"
for /d %%d in ("C:\Program Files\Eclipse Adoptium\jdk-25*") do set "JAVA_EXE=%%d\bin\java.exe"
if not defined JAVA_EXE set "JAVA_EXE=java"
for %%f in (fabric-server*.jar) do (
    "%JAVA_EXE%" -Xms6G -Xmx8G -XX:+UseZGC -XX:+AlwaysPreTouch -jar "%%f" nogui
    goto :end
)
echo [ERROR] No fabric-server*.jar found in %~dp0
:end
pause
