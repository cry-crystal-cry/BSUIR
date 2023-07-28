@echo off
del /q log.txt
rem set /p F1="file1? "
rem set /p F2="file2? "
fc /c %1 %2>log.txt
rem cls если нужно очитстить консоль
set rez=%ErrorLevel% 
if %rez%==2 (
echo compare error
pause
)

if %rez%==1 (
echo files are no the same
del %2% 
attrib +h %1%
pause
)

if %rez%==0 (
echo same files
type %2%
echo.
pause
)