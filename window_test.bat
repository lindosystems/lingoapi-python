ECHO "Testing LINGO API For Windows\n\n\n".>"WindowsTestOutput.txt"

py -3.7 -m venv \myenv37
CALL \myenv37\Scripts\activate.bat
ECHO "Python 3.7\n" >>"WindowsTestOutput.txt"
py  -m pip install numpy
pip install lingo_api
py -m lingo_test >>"WindowsTestOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Transport\
py Transport.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\ErrorTest\
py errorTest.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
CALL \myenv37\Scripts\deactivate.bat

py -3.8 -m venv \myenv38
CALL \myenv38\Scripts\activate.bat
ECHO "Python 3.8\n" >>"WindowsTestOutput.txt"
py  -m pip install numpy
pip install lingo_api
py -m lingo_test >>"WindowsTestOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Transport\
py Transport.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\ErrorTest\
py errorTest.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
CALL \myenv38\Scripts\deactivate.bat

py -3.9 -m venv \myenv39
CALL \myenv39\Scripts\activate.bat
ECHO "Python 3.9\n" >>"WindowsTestOutput.txt"
py  -m pip install numpy
pip install lingo_api
py -m lingo_test >>"WindowsTestOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Transport\
py Transport.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\ErrorTest\
py errorTest.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
CALL \myenv39\Scripts\deactivate.bat

py -3.10 -m venv \myenv310
CALL \myenv310\Scripts\activate.bat
ECHO "Python 3.10\n" >>"WindowsTestOutput.txt"
py  -m pip install numpy
pip install lingo_api
py -m lingo_test >>"WindowsTestOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Transport\
py Transport.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\ErrorTest\
py errorTest.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
CALL \myenv310\Scripts\deactivate.bat

py -3.11 -m venv \myenv311
CALL \myenv311\Scripts\activate.bat
ECHO "Python 3.11\n" >>"WindowsTestOutput.txt"
py  -m pip install numpy
pip install lingo_api
py -m lingo_test >>"WindowsTestOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Transport\
py Transport.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\ErrorTest\
py errorTest.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
CALL \myenv311\Scripts\deactivate.bat

py -3.12 -m venv \myenv312
CALL \myenv312\Scripts\activate.bat
ECHO "Python 3.12\n" >>"WindowsTestOutput.txt"
py  -m pip install numpy
pip install lingo_api
py -m lingo_test >>"WindowsTestOutput.txt"
cd examples\CHESS\
py chess.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Cutting\
py loopCut.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\samsizr\
py samsizr.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\Transport\
py Transport.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
cd examples\ErrorTest\
py errorTest.py >>"..\..\WindowsTestOutput.txt"
cd ..\..
CALL \myenv312\Scripts\deactivate.bat