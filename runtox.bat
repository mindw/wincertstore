@echo off
cls
"c:\Program Files\Python27\Scripts\tox.exe"

echo.
echo --------------
echo Python 2.4 X86
"c:\Program Files (x86)\Python24\python.exe" tests.py

echo.
echo --------------
echo Python 2.5 X86
"c:\Program Files (x86)\Python25\python.exe" tests.py

pause
