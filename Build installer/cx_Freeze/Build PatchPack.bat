set INNO="c:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc

rem set /p VER=<..\..\Version.txt
set VER=0.0.1

echo load version string %VER%

cat AQteck_tool_MAX_PatchPack.iss | sed s/__VERSION__/%VER%/g > AQteck_tool_MAX_PatchPack_with_VERSION.iss

set ISS="AQteck_tool_MAX_PatchPack_with_VERSION.iss"

%INNO% %ISS%