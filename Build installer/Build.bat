set source_folder="..\dist\AQteckModules\_internal\110_device_conf"
set destination_folder="..\dist\AQteckModules\110_device_conf"
xcopy /s /i "%source_folder%" "%destination_folder%\"

set source_folder="..\dist\AQteckModules\_internal\Icons"
set destination_folder="..\dist\AQteckModules\Icons"
xcopy /s /i "%source_folder%" "%destination_folder%\"

set source_folder="..\dist\AQteckModules\_internal\UI"
set destination_folder="..\dist\AQteckModules\UI"
xcopy /s /i "%source_folder%" "%destination_folder%\"

set source_folder="..\dist\AQteckModules\_internal\jsonstyles"
set destination_folder="..\dist\AQteckModules\jsonstyles"
xcopy /s /i "%source_folder%" "%destination_folder%\"

copy "..\dist\AQteckModules\_internal\Version.txt" "..\dist\AQteckModules"

set INNO="c:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc

set ISS="AQteckModules.iss"

%INNO% %ISS%