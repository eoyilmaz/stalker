
@echo off
echo
echo Running nosetest and coverage
echo USAGE doTest [optoinal arguments]
if "%1" == "" (nosetests  --verbosity=2 --with-coverage --cover-package stalker goto end)
echo first aegument %1

:end
echo press any key to exit
pause>null
