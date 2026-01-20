set version=22.0.1
set outputfile=WindowsBuildOutput_%version%.txt

ECHO "Building LINGO API For Windows" >%outputfile%

py -3.7 -m venv \myenv37
CALL \myenv37\Scripts\activate.bat
CALL :build_header %outputfile% 3.7
CALL :old_setup
pip install dist\lingo_api-%version%-cp37-cp37m-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv37\Scripts\deactivate.bat


py -3.8 -m venv \myenv38
CALL \myenv38\Scripts\activate.bat
CALL :build_header %outputfile% 3.8
CALL :old_setup
pip install dist\lingo_api-%version%-cp38-cp38-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv38\Scripts\deactivate.bat

py -3.9 -m venv \myenv39
CALL \myenv39\Scripts\activate.bat
CALL :build_header %outputfile% 3.9
CALL :old_setup
pip install dist\lingo_api-%version%-cp39-cp39-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv39\Scripts\deactivate.bat

py -3.10 -m venv \myenv310
CALL \myenv310\Scripts\activate.bat
CALL :build_header %outputfile% 3.10
CALL :old_setup
pip install dist\lingo_api-%version%-cp310-cp310-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv310\Scripts\deactivate.bat

py -3.11 -m venv \myenv311
CALL \myenv311\Scripts\activate.bat
CALL :build_header %outputfile% 3.11
CALL :new_setup
pip install dist\lingo_api-%version%-cp311-cp311-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv311\Scripts\deactivate.bat

py -3.12 -m venv \myenv312
CALL \myenv312\Scripts\activate.bat
CALL :build_header %outputfile% 3.12
CALL :new_setup
pip install dist\lingo_api-%version%-cp312-cp312-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv312\Scripts\deactivate.bat


py -3.13 -m venv \myenv313
CALL \myenv313\Scripts\activate.bat
CALL :build_header %outputfile% 3.13
CALL :new_setup
pip install dist\lingo_api-%version%-cp313-cp313-win_amd64.whl
CALL :run_tests %outputfile%
CALL \myenv313\Scripts\deactivate.bat

REM Done with build/test
GOTO :EOF


:build_header
ECHO. >>%~1
ECHO "==============================================================" >>%~1
ECHO "Python %~2" >>%~1
ECHO "==============================================================" >>%~1
ECHO. >>%~1

:old_setup
REM Use to build lingo for python 3.7-3.10
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
pip install importlib-metadata
py  -m pip install numpy
py  -m pip install pandas
python -m build
GOTO :EOF


:new_setup
REM Use to build lingo for py 3.11 and later
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py  -m pip install pandas
pip install importlib-metadata
py setup.py bdist_wheel
GOTO :EOF


:run_tests
ECHO "Testing installation..." >>%-1
py -m lingo_test >>%-1

ECHO "Chess.py" >>%-1
cd examples\CHESS\
py chess.py >>"..\..\%~1"
cd ..\..

ECHO "LoopCut.py" >>%-1
cd examples\Cutting\
py loopCut.py >>"..\..\%~1"
cd ..\..

ECHO "Samsizr.py" >>%-1
cd examples\samsizr\
py samsizr.py >>"..\..\%~1"
cd ..\..

ECHO "Transport.py" >>%-1
cd examples\Transport\
py Transport.py >>"..\..\%~1"
cd ..\..

ECHO "PORTCardCor.py" >>%-1
cd examples\PORTCardCor\
py port.py >>"..\..\%~1"
cd ..\..

ECHO "ErrorTest.py" >>%-1
cd examples\ErrorTest\
py errorTest.py >>"..\..\%~1"
cd ..\..
GOTO :EOF
