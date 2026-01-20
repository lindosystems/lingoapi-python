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
        self.MAJOR = "22"
        self.MINOR = "0"
        self.LINGO_HOME = os.environ.get('LINGO_22_HOME')
        self.LINGO64_HOME = os.environ.get('LINGO64_22_HOME')
        self.platform = platform.system()
        self.is_64bits = sys.maxsize > 2**32
        self.pyMajor = sys.version_info[0]
        self.pyMinor = sys.version_info[1]
    """
        Return string for a print 
        used for debugging
    """
    def __str__(self):
        return f"\
            Build Data\n\
            LINGO {self.MAJOR}.{self.MINOR}\n\
            Python {self.pyMajor}.{self.pyMinor}\n\
            LINGO Home Dir:\n\
            \t64-bit = {self.LINGO64_HOME}\n\
            \t32-bit = {self.LINGO_HOME}\n\
            Turn off when done debugging\n\
        "
    
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
    else:
        if bd.is_64bits:
            os.environ['PATH'] = bd.LINGO64_HOME + os.pathsep + os.environ['PATH']
        else:
            os.environ['PATH'] = bd.LINGO_HOME + os.pathsep + os.environ['PATH']

#
# linux()
# This function loads the libirc.so from the appropriate bin dir
#
def linux(bd:BuildData):
    
    libircPath = os.path.join(bd.LINGO64_HOME,"bin/linux64/libirc.so")
    try:
        cdll.LoadLibrary(libircPath)
    except Exception as e:
        customException =  LoadException()
        print(customException.errorMessage)
        print("Python Error: ", e)
        exit()


    
def main():
    bd = BuildData()
    ## print(bd) # If Debug
    #Environment variable LINDOAPI_HOME must be set
    if bd.LINGO_HOME == None and bd.is_64bits == False:
        raise NoEviromentVar("LINGO_22_HOME", "Lingo22")

    if bd.LINGO64_HOME == None and bd.is_64bits:
        raise NoEviromentVar("LINGO64_22_HOME", "Lingo64_22")

    if bd.platform == 'Windows' or bd.platform == "CYGWIN_NT-6.3":
        windows(bd)
    else:
        linux(bd)
main()