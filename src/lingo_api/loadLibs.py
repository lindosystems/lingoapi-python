from .lingoExceptions import * 
import os
import sys
import platform
from ctypes import cdll

class BuildData():
    """
    BuildData()

    A class for holding data about Operating system
    and Lindo location/ version

    """
    def __init__(self):
        self.MAJOR = "19"
        self.MINOR = "0"
        self.LINGO_HOME = os.environ.get('LINGO_19_HOME')
        self.LINGO64_HOME = os.environ.get('LINGO64_19_HOME')
        self.platform = platform.system()
        self.is_64bits = sys.maxsize > 2**32
        self.pyMajor = sys.version_info[0]
        self.pyMinor = sys.version_info[1]

#
# windows()
# This function adds the dll directory at 
# runtime
def windows(bd:BuildData):

    if (bd.pyMajor == 3) and (bd.pyMinor != 7):
        if bd.is_64bits:
            os.add_dll_directory(bd.LINGO64_HOME)
        else:
            os.add_dll_directory(bd.LINGO_HOME)

#
# linux()
# This function loads the libirc.so from the appropriate bin dir
#
def linux(bd:BuildData):

    libircPath = os.path.join(bd.LINGO_HOME,"bin/linux64/libirc.so")
    try:
        if os.path.isfile(libircPath):
            cdll.LoadLibrary(libircPath)
        else:
            raise LoadException
    except LoadException as e:
        print(e.errorMessage)
        exit(1)


    
def main():
    bd = BuildData()
    #Environment variable LINDOAPI_HOME must be set
    if bd.LINGO_HOME == None and bd.is_64bits == False:
        raise NoEviromentVar("LINGO_19_HOME", "Lingo19")
        exit(0)
    if bd.LINGO64_HOME == None and bd.is_64bits:
        raise NoEviromentVar("LINGO64_19_HOME", "Lingo64_19")
        exit(0)
    if bd.platform == 'Windows' or bd.platform == "CYGWIN_NT-6.3":
        windows(bd)
    else:
        linux(bd)
main()