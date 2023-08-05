if exist %USERPROFILE%\Anaconda3\python.exe (
	echo Found %USERPROFILE%\Anaconda3\python.exe
	set ANACONDA_LOCATION=%USERPROFILE%\Anaconda3
	echo %ANACONDA_LOCALTION%
    call %ANACONDA_LOCATION%\Scripts\activate.bat
) else if exist  %USERPROFILE\AppData\Local\Continuum\Anaconda3\python.exe (
	echo "Found %USERPROFILE\AppData\Local\Continuum\Anaconda3\python.exe
	set ANACONDA_LOCATION=%USERPROFILE%\AppData\Local\Continuum\Anaconda3"
	echo %ANACONDA_LOCALTION%
    call %ANACONDA_LOCATION%\Scripts\activate.bat
) else (
	rem "Cannot find Anaconda Python"
	exit /b 2
)    
    
call conda activate s33specimagesum

python -m s33specimagesum