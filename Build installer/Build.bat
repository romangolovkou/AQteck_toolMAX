set source_folder="..\dist\AQteck tool MAX\_internal\110_device_conf"
set destination_folder="..\dist\AQteck tool MAX\110_device_conf"
xcopy /s /i %source_folder% %destination_folder%

set source_folder="..\dist\AQteck tool MAX\_internal\Icons"
set destination_folder="..\dist\AQteck tool MAX\Icons"
xcopy /s /i %source_folder% %destination_folder%

set source_folder="..\dist\AQteck tool MAX\_internal\UI"
set destination_folder="..\dist\AQteck tool MAX\UI"
xcopy /s /i %source_folder% %destination_folder%

set source_folder="..\dist\AQteck tool MAX\_internal\jsonstyles"
set destination_folder="..\dist\AQteck tool MAX\jsonstyles"
xcopy /s /i %source_folder% %destination_folder%

copy "..\dist\AQteck tool MAX\_internal\Version.txt" "..\dist\AQteck tool MAX"

set INNO="c:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc

set ISS="AQteck tool MAX.iss"

%INNO% %ISS%