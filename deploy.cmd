set dest=%userprofile%\AppData\Local\EDMarketConnector\plugins\EDMFAT
copy %dest%\settings.json %temp%
rd /s /q %dest%
mkdir %dest%
xcopy /y load.py %dest%
xcopy /y web_services.py %dest%
xcopy /y checklistbox.py %dest%
mkdir %dest%\edmfs
xcopy /s /y edmfs\*.py %dest%\edmfs 
copy %temp%\settings.json %dest%
