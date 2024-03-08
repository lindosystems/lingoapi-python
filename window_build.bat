set version=21.0.7
set outputfile=\WindowsBuildOutput.txt

ECHO "Building LINGO API For Windows\n\n\n".>"WindowsBuildOutput.txt"

py -3.7 -m venv \myenv37
CALL \myenv37\Scripts\activate.bat
ECHO "Python 3.7\n" >>"WindowsBuildOutput.txt"
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py setup.py bdist_wheel
pip install dist\lingo_api-%version%-cp37-cp37m-win_amd64.whl
py -m lingo_test >>"WindowsBuildOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
CALL \myenv37\Scripts\deactivate.bat

py -3.8 -m venv \myenv38
CALL \myenv38\Scripts\activate.bat
ECHO "Python 3.8\n" >>"WindowsBuildOutput.txt"
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py setup.py bdist_wheel
pip install dist\lingo_api-%version%-cp38-cp38-win_amd64.whl
py -m lingo_test >>"WindowsBuildOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
CALL \myenv38\Scripts\deactivate.bat

py -3.9 -m venv \myenv39
CALL \myenv39\Scripts\activate.bat
ECHO "Python 3.9\n" >>"WindowsBuildOutput.txt"
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py setup.py bdist_wheel
pip install dist\lingo_api-%version%-cp39-cp39-win_amd64.whl
py -m lingo_test >>"WindowsBuildOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
CALL \myenv39\Scripts\deactivate.bat

py -3.10 -m venv \myenv310
CALL \myenv310\Scripts\activate.bat
ECHO "Python 3.10\n" >>"WindowsBuildOutput.txt"
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py setup.py bdist_wheel
pip install dist\lingo_api-%version%-cp310-cp310-win_amd64.whl
py -m lingo_test >>"WindowsBuildOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
CALL \myenv310\Scripts\deactivate.bat

py -3.11 -m venv \myenv311
CALL \myenv311\Scripts\activate.bat
ECHO "Python 3.11\n" >>"WindowsBuildOutput.txt"
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py setup.py bdist_wheel
pip install dist\lingo_api-%version%-cp311-cp311-win_amd64.whl
py -m lingo_test >>"WindowsBuildOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
CALL \myenv311\Scripts\deactivate.bat

py -3.12 -m venv \myenv312
CALL \myenv312\Scripts\activate.bat
ECHO "Python 3.12\n" >>"WindowsBuildOutput.txt"
py -m pip install build
py  -m pip install setuptools
py  -m pip install wheel
py  -m pip install numpy
py setup.py bdist_wheel
pip install dist\lingo_api-%version%-cp312-cp312-win_amd64.whl
py -m lingo_test >>"WindowsBuildOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsBuildOutput.txt"
cd ..\..
CALL \myenv312\Scripts\deactivate.bat