
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
..\Scripts\nosetests --processes=4 --verbosity=2 tests/ext/test_auth.py
goto end
:all
..\Scripts\nosetests --processes=4 --verbosity=2 tests
goto end 
:end
echo press any key to exit
pause>null
