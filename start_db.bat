@echo off
echo Starting PostgreSQL 18...
"C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe" start -D "C:\Program Files\PostgreSQL\18\data" -l "d:\avrasya_site\pg_server.log"
echo Done.
pause
