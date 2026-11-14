@echo off
cd /d "D:\Minecraft Server"
for /d %%d in ("C:\Program Files\Eclipse Adoptium\jdk-25*") do set "JAVA_EXE=%%d\bin\java.exe"
for %%f in (fabric-server*.jar) do (
    "%JAVA_EXE%" -Xms6G -Xmx8G -XX:+UseZGC -XX:+AlwaysPreTouch -jar "%%f" nogui
    goto :end
)
:end
pause