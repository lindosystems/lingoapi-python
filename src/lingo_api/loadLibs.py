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
        self.platform = platform.system()
        self.is_64bits = sys.maxsize > 2**32

#
# windows()
# This function adds the dll directory at 
# runtime
def windows(bd:BuildData):
    if (sys.version_info[0] == 3) and (sys.version_info[1] != 7):
        os.add_dll_directory(bd.LINGO_HOME)

#
# linux()
# This function loads the libirc.so from the appropriate bin dir
#
def linux(bd:BuildData):
    if bd.is_64bits:
        cdll.LoadLibrary(os.path.join(bd.LINGO_HOME,"bin/linux64/libirc.so"))
    else:
        cdll.LoadLibrary(os.path.join(bd.LINGO_HOME,"bin/linux/libirc.so"))


    
def main():
    bd = BuildData()
    #Environment variable LINDOAPI_HOME must be set
    if bd.LINGO_HOME == None:
        print("Environment variable LINDOAPI_HOME should be set!")
        exit(0)
    if bd.platform == 'Windows' or bd.platform == "CYGWIN_NT-6.3":
        windows(bd)
    else:
        linux(bd)
main()