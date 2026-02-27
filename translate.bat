@echo off
set PY=.\Env\Scripts\python.exe
set IGN=--ignore Env/* --ignore venv/* --ignore .venv/* --ignore staticfiles/* --ignore media/*

echo Updating Turkish messages...
%PY% manage.py makemessages -l tr %IGN%

echo Updating English messages...
%PY% manage.py makemessages -l en %IGN%

echo Updating Persian messages...
%PY% manage.py makemessages -l fa %IGN%

echo Updating Arabic messages...
%PY% manage.py makemessages -l ar %IGN%

echo Updating Russian messages...
%PY% manage.py makemessages -l ru %IGN%

echo Updating German messages...
%PY% manage.py makemessages -l de %IGN%

echo.
echo All languages updated! Now edit your .po files and then run:
echo %PY% manage.py compilemessages
pause
