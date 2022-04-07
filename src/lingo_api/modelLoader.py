from .const           import *
from .lingoExceptions import *
from .lingo           import *
import numpy as np

class Model():

    def __init__(self, lngFile, pointerDict, logFile=None):

        self.lngFile     = lngFile
        self.pointerDict = pointerDict
        self.logFile     = logFile
        self._changedDict = {}

    def get_lngFile(self):
        """get_lngFile returns lngFile"""
        return self.lngFile

    def get_pointerDict(self):
        """get_pointerDict returns pointerDict"""
        return self.pointerDict

    def get_logFile(self):
        """get_logFile returns logFile"""
        return self.logFile

    def get_pointer(self, key):
        """get_pointer returns the poiner from key in pointerDict
            Arguments: 
                key -- a key in the pointerDict """
        return self.pointerDict[key]

    def set_lngFile(self,lngFile):
        """set_lngFile sets the lngFile"""
        self.lngFile = lngFile

    def set_pointerDict(self,pointerDict):
        """set_pointerDict sets the pointerDict"""
        self.pointerDict = pointerDict

    def set_logFile(self,logFile):
        """set_logFile sets the logFile"""
        self.logFile = logFile
    def set_pointer(self, key, pointer):
        """set_pointer """
        self.pointerDict[key] = pointer


# TODO: Add Callback support once callbacks are added to pyLingo.c
# # MyCallback( void* pModel, int nReserved, void* pUserData)
# def defult_cbSolver(pEnv, nReserved, pUserData):
#     pass

# # int LSsetCallbackErrorLng( pLSenvLINGO pL, lngCBFuncError_t pcbf, void* pUserData)
# def defult_cbError(pEnv, nReserved, pUserData):
#     pass


def solve(lm:Model):
    """
    solve sends a Model object to the Lingo API to be solved
        Arguments: 
        lm -- a Model object
        Returns:
        0 -- If success
        raises LingoError if something goes wrong with API call.
        raises TypeNotSupportedError if a pointer type is passed that is
            not supported by the Lingo API.
    """
    #create Lingo enviroment object
    pEnv = pyLScreateEnvLng()
    if pEnv is None:
        raise LingoError(errorcode)


    # open LINGO's log file
    if lm.logFile != None:
        errorcode = pyLSopenLogFileLng(pEnv, lm.logFile)
        if errorcode != LSERR_NO_ERROR_LNG:
            raise LingoError(errorcode)
    

    # pass memory transfer pointers to LINGO
    pnPointersNow = np.array([0],dtype=np.int32)
    # Loop over dict
    for key, pointer in lm.pointerDict.items():
        
        # needs to be a numpy array?
        # can be a list?
        # can be a number? 
        if type(pointer)!=np.ndarray:
            if type(pointer)==int or type(pointer)==float or isinstance(pointer, np.number):
                lm._changedDict[key] = type(pointer)
                pointer = np.array([pointer], dtype=np.double)
                lm.set_pointer(key, pointer)
            elif type(pointer)==list:
                lm._changedDict[key] = type(pointer)
                pointer = np.array(pointer, dtype=np.double)
                lm.set_pointer(key, pointer)
            else:
                error = f"{key} {pointer} type: {type(pointer)}"
                raise TypeNotSupportedError(error) 
        # 2 needs to be converted to dtype=numpy.double if not already
        if pointer.dtype!=np.double:
            lm._changedDict[key] = pointer.dtype
            pointer = pointer.astype(np.double)
            lm.set_pointer(key, pointer)
        # 3 possibly flattened if not already
        if pointer.ndim > 1:
            pointer = pointer.flatten()
            lm.set_pointer(key, pointer)
        # more?
        # send pointer to Lingo
        errorcode = pyLSsetDouPointerLng(pEnv, pointer, pnPointersNow)
        if errorcode != LSERR_NO_ERROR_LNG:
            raise LingoError(errorcode)

    #Run the script
    cScript = "SET ECHOIN 1 \n TAKE "+lm.lngFile+" \n GO \n QUIT \n"
    errorcode = pyLSexecuteScriptLng(pEnv, cScript)
    if errorcode != LSERR_NO_ERROR_LNG:
        raise LingoError(errorcode)

    #Close the log file
    if lm.logFile != None:
        errorcode = pyLScloseLogFileLng(pEnv)
        if errorcode != LSERR_NO_ERROR_LNG:
            raise LingoError(errorcode)

    #delete Lingo enviroment object
    errorcode = pyLSdeleteEnvLng(pEnv)
    if errorcode != LSERR_NO_ERROR_LNG:
        raise LingoError(errorcode)

    _resetChanges(lm)
    
    return 0

def _resetChanges(lm:Model):
    for key, t in lm._changedDict.items():
        pointer = lm.get_pointer(key)
        if t == list:
            pointer = pointer.tolist()
            lm.set_pointer(key, pointer)
        elif t == float:
            lm.set_pointer(key, pointer[0])
        elif t == int:
            lm.set_pointer(key, int(pointer[0]))
        else:
            lm.set_pointer(key, pointer.astype(t)) # if it is some casted numpy type

            
            