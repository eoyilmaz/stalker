
@echo off

:start
CLS
echo Running nosetests and coverage
echo ---------------------------------------------------------------------
echo Press 1 to Start auth test
echo Press 2 to do all tests
set /P F= 
if %F%==1 goto auth
if %F%==2  goto all
rem 
:auth
nosetests  --verbosity=2 --with-coverage tests/ext/test_auth.py 
goto end
:all
nosetests  --verbosity=2 --with-coverage --cover-package tests
goto end 
:end
echo press any key to exit
pause>null
