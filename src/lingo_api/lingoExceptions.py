from .const     import *
import os
import sys
import platform

class lingoException(Exception):
    """
    Base class fo Lingo errors that a Base class itself of Exception
    """
    def __init__(self, error, message):
        self.error = error
        self.message = message
    def __str__(self):
        return f"{self.error} -> {self.message}"

class TypeNotSupportedError(lingoException):
    """ Exception rasied for sending an unsupported datatype as a pointer
        error: a discrtipion of what rasied the error
    """
    def __init__(self, error):
        self.error = error
        self.message = "Unsupported type\nPrefered type: Numpy Array of np.double\nOther excepted: Int, floats, lists of Ints or floats"
                
class LingoError(lingoException):
    """ Exception rasied for errors thrown by the API
    Attributes:
    error: The error number returned by a Lingo API function
    """

    def __init__(self, error):
        self.error = error
        self.message   = ErrorDict[error]



class LoadException():
    """ Exception raised for errors in loading DLLs or SO files """

    def __init__(self):

        self.LINGO_HOME   = os.environ.get('LINGO_19_HOME')
        self.platform     = platform.system()
        self.is_64bits    = sys.maxsize > 2**32
        self.errorMessage = self.getMessage()

    def getMessage(self):

        if self.platform == 'Windows' or self.platform == "CYGWIN_NT-6.3":
            msg = "Lingo Import Error:                                                          \n\
                        Make sure all the following files are present in "+ self.LINGO_HOME  +":\n\
                        Chartdir60.dll                                                          \n\
                        Cilkrts20.dll                                                           \n\
                        Conopt3.dll                                                             \n\
                        Conopt464.dll                                                           \n\
                        Libifcoremd.dll                                                         \n\
                        Libiomp5md.dll                                                          \n\
                        Libmmd.dll                                                              \n\
                        Lindo64_13_0.dll                                                        \n\
                        Lindopr64_8.dll                                                         \n\
                        Lingd64_19.dll                                                          \n\
                        Lingdb64_3.dll                                                          \n\
                        Lingf64_19.dll                                                          \n\
                        Lingfd64_19.dll                                                         \n\
                        Lingj64_19.dll                                                          \n\
                        Lingoau64_14.dll                                                        \n\
                        Lingr64_1.dll                                                           \n\
                        Lingxl64_5.dll                                                          \n\
                        Mosek64_9_2.dll                                                         \n\
                        Msvcr120.dll                                                            \n\
                    "

        elif self.is_64bits:
            pathTolibs = os.path.join(self.LINGO_HOME,"bin/linux64/")
            msg = "Lingo Import Error:                                                            \n\
                        Make sure all the following files are present in "+ pathTolibs  + ":      \n\
                        libQt5Core.so.5                                                           \n\
                        libQt5Core.so.5.2                                                         \n\
                        libQt5Core.so.5.2.1                                                       \n\
                        libQt5Gui.so.5                                                            \n\
                        libQt5Gui.so.5.2                                                          \n\
                        libQt5Gui.so.5.2.1                                                        \n\
                        libQt5PrintSupport.so.5                                                   \n\
                        libQt5PrintSupport.so.5.2                                                 \n\
                        libQt5PrintSupport.so.5.2.1                                               \n\
                        libQt5Widgets.so.5                                                        \n\
                        libQt5Widgets.so.5.2                                                      \n\
                        libQt5Widgets.so.5.2.1                                                    \n\
                        libchartdir.so                                                            \n\
                        libchartdir.so.6                                                          \n\
                        libchartdir.so.6.0                                                        \n\
                        libcilkrts.so                                                             \n\
                        libcilkrts.so.5                                                           \n\
                        libconopt464.so                                                           \n\
                        libconsub3.so                                                             \n\
                        libgcc_s.so.1                                                             \n\
                        libgfortran.so                                                            \n\
                        libgfortran.so.5                                                          \n\
                        libgomp.so.1                                                              \n\
                        libifcoremt.so                                                            \n\
                        libifcoremt.so.5                                                          \n\
                        libifport.so                                                              \n\
                        libifport.so.5                                                            \n\
                        libimf.so                                                                 \n\
                        libintlc.so                                                               \n\
                        libintlc.so.5                                                             \n\
                        libiomp5.so                                                               \n\
                        libirc.so                                                                 \n\
                        liblindo64.so                                                             \n\
                        liblindo64.so.13                                                          \n\
                        liblindo64.so.13.0                                                        \n\
                        liblingo64.so                                                             \n\
                        liblingo64.so.19                                                          \n\
                        liblingo64.so.19.0                                                        \n\
                        liblingogui64.so                                                          \n\
                        liblingogui64.so.19                                                       \n\
                        liblingogui64.so.19.0                                                     \n\
                        liblingojni64.so                                                          \n\
                        liblingojni64.so.19                                                       \n\
                        liblingojni64.so.19.0                                                     \n\
                        libmosek64.so                                                             \n\
                        libmosek64.so.9                                                           \n\
                        libmosek64.so.9.2                                                         \n\
                        libquadmath.so.0                                                          \n\
                        libsvml.so                                                                \n\
                        "
        else:
            pathTolibs = os.path.join(self.LINGO_HOME,"bin/linux/")
            msg = "Lingo Import Error:                                                            \n\
                        Make sure all the following files are present in "+ pathTolibs  + ":      \n\
                        libQt5Core.so.5                                                           \n\
                        libQt5Core.so.5.2                                                         \n\
                        libQt5Core.so.5.2.1                                                       \n\
                        libQt5Gui.so.5                                                            \n\
                        libQt5Gui.so.5.2                                                          \n\
                        libQt5Gui.so.5.2.1                                                        \n\
                        libQt5PrintSupport.so.5                                                   \n\
                        libQt5PrintSupport.so.5.2                                                 \n\
                        libQt5PrintSupport.so.5.2.1                                               \n\
                        libQt5Widgets.so.5                                                        \n\
                        libQt5Widgets.so.5.2                                                      \n\
                        libQt5Widgets.so.5.2.1                                                    \n\
                        libchartdir.so                                                            \n\
                        libchartdir.so.6                                                          \n\
                        libchartdir.so.6.0                                                        \n\
                        libcilkrts.so                                                             \n\
                        libcilkrts.so.5                                                           \n\
                        libconopt464.so                                                           \n\
                        libconsub3.so                                                             \n\
                        libgcc_s.so.1                                                             \n\
                        libgfortran.so                                                            \n\
                        libgfortran.so.5                                                          \n\
                        libgomp.so.1                                                              \n\
                        libifcoremt.so                                                            \n\
                        libifcoremt.so.5                                                          \n\
                        libifport.so                                                              \n\
                        libifport.so.5                                                            \n\
                        libimf.so                                                                 \n\
                        libintlc.so                                                               \n\
                        libintlc.so.5                                                             \n\
                        libiomp5.so                                                               \n\
                        libirc.so                                                                 \n\
                        liblindo.so                                                               \n\
                        liblindo.so.13                                                            \n\
                        liblindo.so.13.0                                                          \n\
                        liblingo.so                                                               \n\
                        liblingo.so.19                                                            \n\
                        liblingo.so.19.0                                                          \n\
                        liblingogui.so                                                            \n\
                        liblingogui.so.19                                                         \n\
                        liblingogui.so.19.0                                                       \n\
                        liblingojni.so                                                            \n\
                        liblingojni.so.19                                                         \n\
                        liblingojni.so.19.0                                                       \n\
                        libmosek.so                                                               \n\
                        libmosek.so.9                                                             \n\
                        libmosek.so.9.2                                                           \n\
                        libquadmath.so.0                                                          \n\
                        libsvml.so                                                                \n\
                        "
        return msg



