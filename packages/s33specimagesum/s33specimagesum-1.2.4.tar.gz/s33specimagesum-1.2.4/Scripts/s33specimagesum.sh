#! /bin/bash
if [ -f %USERPROFILE%\Anaconda3\python];
	ANACONDA_LOCATION=%USERPROFILE%\Anaconda3
    %ANACONDA_LOCATION%\Scripts\activate

elif if exist  %USERPROFILE\AppData\Local\Continuum\Anaconda3\python.exe (
	ANACONDA_LOCATION=%USERPROFILE%\AppData\Local\Continuum\Anaconda3"
    call %ANACONDA_LOCATION%\Scripts\activate.bat
else (
	rem "Cannot find Anaconda Python"
	exit /b 2
fi    

conda activate s33specimagesum

python -m 33specimagesum