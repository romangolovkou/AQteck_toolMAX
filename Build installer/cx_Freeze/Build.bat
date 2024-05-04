set INNO="c:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc

set /p VER=<..\..\Version.txt

echo load version string %VER%

cat AQteck_tool_MAX_for_cx_Freeze.iss | sed s/__VERSION__/%VER%/g > AQteck_tool_MAX_for_cx_Freeze_with_VERSION.iss

set ISS="AQteck_tool_MAX_for_cx_Freeze_with_VERSION.iss"

%INNO% %ISS%