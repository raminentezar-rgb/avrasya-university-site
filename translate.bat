@echo off
echo Updating Persian messages...
.\Env\Scripts\python.exe manage.py makemessages -l fa
echo Updating English messages...
.\Env\Scripts\python.exe manage.py makemessages -l en
echo Updating Turkish messages...
.\Env\Scripts\python.exe manage.py makemessages -l tr
echo.
echo All languages updated! Now edit your .po files and then run: 
echo .\Env\Scripts\python.exe manage.py compilemessages
pause