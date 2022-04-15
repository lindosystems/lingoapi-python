from pickle import NONE
from time import process_time_ns
from tkinter.messagebox import NO
from traceback import print_tb
from .const           import *
from .lingoExceptions import *
from .lingo           import *
import numpy as np



class Model():

    def __init__(self, lngFile, pointerDict, logFile=None,
                 cbSolver=None, cbError=None,
                 uData=None):

        self.lngFile     = lngFile
        self.pointerDict = pointerDict
        self.logFile     = logFile
        self.cbSolver    = cbSolver
        self.cbError     = cbError
        self.uData       = uData

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

    def get_cbSolver(self):
        """get_cbSolver returns the solver callback"""
        return self.cbSolver

    def get_cbError(self):
        """get_cbError returns error callback"""
        return self.cbError

    def get_uData(self):
        """get_uData returns uData dictionary"""
        return self.uData

    def set_lngFile(self,lngFile):
        """set_lngFile sets the lngFile"""
        self.lngFile = lngFile

    def set_pointerDict(self,pointerDict):
        """set_pointerDict sets the pointerDict"""
        self.pointerDict = pointerDict

    def set_logFile(self,logFile):
        """set_logFile sets the logFile"""
        self.logFile = logFile

    def set_pointer(self,key,pointer):
        """set_pointer """
        self.pointerDict[key] = pointer

    def set_cbSolver(self,cbSolver):
        """set_cbSolver sets the solver callback"""
        self.cbSolver = cbSolver

    def set_cbError(self,cbError):
        """get_cbError sets error callback"""
        self.cbError = cbError

    def set_uData(self,uData):
        """get_uData sets uData dictionary"""
        self.uData = uData




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

    # set callbacks if passed
    if lm.cbError != None and lm.uData != None:
        errorcode = pyLSsetCallbackErrorLng(pEnv, lm.cbError, lm.uData)
        if errorcode != LSERR_NO_ERROR_LNG:
            raise LingoError(errorcode)
    if lm.cbSolver != None and lm.uData != None:
        errorcode = pyLSsetCallbackSolverLng(pEnv, lm.cbSolver, lm.uData)
        if errorcode != LSERR_NO_ERROR_LNG:
            raise LingoError(errorcode)


    
    

        
    # pass memory transfer pointers to LINGO
    pnPointersNow = np.array([0],dtype=np.int32)
    # Loop over dict

        
    for key, pointer in lm.pointerDict.items():
        
        # except arrays and singletons
        if type(pointer)==int or type(pointer)==float  or isinstance(pointer, np.number):
            lm._changedDict[key] = type(pointer)
            pointer = np.array([pointer], dtype=np.double)
            lm.set_pointer(key, pointer)
        # After this point everything should be a np array
        if type(pointer) != np.ndarray:
                error = f"{key} {pointer} type: {type(pointer)}"
                raise TypeNotSupportedError(error) 
        # The np array can not be empty
        if len(pointer) == 0:
            raise EmptyPointer(key)
        
        # Make sure all Arrays are flat
        if pointer.ndim > 1:
            pointer = pointer.flatten()
            lm.set_pointer(key, pointer) # try without this line too...

        # Fix string arrays
        if isinstance(pointer[0], np.character):
            tempPointerStr = ""
            tempPointerArr = np.array([""], dtype='S1024')
            for i in range(0,len(pointer)):
                tempPointerStr+=f"{pointer[i]} \n "
            tempPointerArr[0] = tempPointerStr
            errorcode = pyLSsetCharPointerLng(pEnv, tempPointerArr, pnPointersNow)
            if errorcode != LSERR_NO_ERROR_LNG:
                raise LingoError(errorcode)
        else:
            if pointer.dtype!=np.double:
                lm._changedDict[key] = pointer.dtype
                pointer = pointer.astype(np.double)
                lm.set_pointer(key, pointer)
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
        if t == float:
            lm.set_pointer(key, pointer[0])
        elif t == int:
            lm.set_pointer(key, int(pointer[0]))
        else:
            lm.set_pointer(key, pointer.astype(t)) # if it is some casted numpy type

            
            