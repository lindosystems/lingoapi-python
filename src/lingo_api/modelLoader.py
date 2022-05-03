from pyexpat import model
from traceback import print_tb
from .const           import *
from .lingoExceptions import *
from .lingo           import *
import numpy as np

class Model():

    def __init__(self, lngFile, logFile="TempModel.log",
                 cbSolver=None, cbError=None,
                 uData=None):

        self.lngFile     = lngFile
        self.logFile     = logFile
        self.cbSolver    = cbSolver
        self.cbError     = cbError
        self.uData       = uData

        self._pointerDict = {}
        self._changedDict = {}

    def get_lngFile(self):
        """get_lngFile returns lngFile"""
        return self.lngFile

    def get_pointerDict(self):
        """get_pointerDict returns pointerDict"""
        return self._pointerDict

    def get_logFile(self):
        """get_logFile returns logFile"""
        return self.logFile

    def get_pointer(self, ptrName):
        """get_pointer returns the poiner from key in pointerDict
            Arguments: 
                key -- a key in the pointerDict """
        return self._pointerDict[ptrName]

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

    def set_logFile(self,logFile):
        """set_logFile sets the logFile"""
        self.logFile = logFile

    def set_pointer(self,key,pointer, type):
        """set_pointer """
        self._pointerDict[key] = (pointer, type)

    def set_cbSolver(self,cbSolver):
        """set_cbSolver sets the solver callback"""
        self.cbSolver = cbSolver

    def set_cbError(self,cbError):
        """set_cbError sets error callback"""
        self.cbError = cbError

    def set_uData(self,uData):
        """set_uData sets uData dictionary"""
        self.uData = uData

    def __str__(self):

        modelStr = f"Lingo Model {self.lngFile}\nPointers Set:"
        for key, tuple in self._pointerDict.items():
            try:
                ptrType = PtrTypeDict[tuple[1]]
            except Exception:
                ptrType = tuple[1] 

            modelStr += f"\nName :{key}\nType :{ptrType}\nData :{tuple[0]}\n"
        return modelStr



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
    if lm.cbSolver != None and lm.uData != None:
        errorcode = pyLSsetCallbackSolverLng(pEnv, lm.cbSolver, lm.uData)
        if errorcode != LSERR_NO_ERROR_LNG:
                raise LingoError(errorcode)

    if lm.cbError != None and lm.uData != None:
        errorcode = pyLSsetCallbackErrorLng(pEnv, lm.cbError, lm.uData)
        if errorcode != LSERR_NO_ERROR_LNG:
            raise LingoError(errorcode)




    # pass memory transfer pointers to LINGO
    pnPointersNow = np.array([0],dtype=np.int32)
    # Loop over dict

    for key, tuple in lm._pointerDict.items():
        

        pointer = tuple[0]
        ptrType = tuple[1]


        # set Param and Vars as np.double
        # except arrays and singletons
        if type( pointer)==int or type( pointer)==float  or isinstance(pointer, np.number):
            lm._changedDict[key] = type( pointer)
            pointer = np.array([pointer], dtype=np.double)
            lm.set_pointer(key, pointer, ptrType)
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
            lm.set_pointer(key, pointer, ptrType) # try without this line too...

        # set Sets as "|S" type
        if ptrType == SET:
            tempPointerArrstr = ""
            for i in range(0,len(pointer)):
                tempPointerArrstr+=f"{str(pointer[i])}\n"
            tempPointerArr = np.array([tempPointerArrstr])
            byteSize = 2*len(tempPointerArr[0]) #<- doubling the len to determin the byte size for the np array
            tempPointerArr = tempPointerArr.astype(f"|S{byteSize}")
            errorcode = pyLSsetCharPointerLng(pEnv, tempPointerArr, pnPointersNow)
            if errorcode != LSERR_NO_ERROR_LNG:
                raise LingoError(errorcode)

        elif ptrType == PARAM or ptrType == VAR:
            if pointer.dtype!=np.double:
                lm._changedDict[key] = pointer.dtype
                pointer = pointer.astype(np.double)
                lm.set_pointer(key, pointer, ptrType)
            errorcode = pyLSsetDouPointerLng(pEnv, pointer, pnPointersNow)
            if errorcode != LSERR_NO_ERROR_LNG:
                raise LingoError(errorcode)
        else:
            raise PointerTypeNotSupportedError(ptrType)
          

    #Run the script
    cScript = "SET ECHOIN 1 \n TAKE "+lm.lngFile+" \n GO \n QUIT \n"
    errorcode = pyLSexecuteScriptLng(pEnv, cScript)
    if errorcode != LSERR_NO_ERROR_LNG:
        errorcode2 = pyLScloseLogFileLng(pEnv)
        errorcode3 = pyLSdeleteEnvLng(pEnv)
        _resetChanges(lm)
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
        pointer, ptrType = lm.get_pointer(key)
        if t == float:
            lm.set_pointer(key, pointer[0], ptrType)
        elif t == int:
            lm.set_pointer(key, int(pointer[0]), ptrType)
        else:
            lm.set_pointer(key, pointer.astype(t), ptrType) # if it is some casted numpy type

            
            