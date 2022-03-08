#  A Python programming example of interfacing with LINGO API.
#  An application to the Acceptance Sampling Designp.
import lingo_api as lingo
import numpy as np
import sys

def samsizr(AQL,LTFD,PRDRISK,CONRISK,MINSMP,MAXSMP):

    #create Lingo enviroment object
    pEnv = lingo.pyLScreateEnvLng()
    if pEnv is None:
        print("cannot create LINGO environment!")
        exit(1)

    #open LINGO's log file
    errorcode = lingo.pyLSopenLogFileLng(pEnv,'samsizr.log')
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #pass memory transfer pointers to LINGO
    #define pnPointersNow
    pnPointersNow = np.array([0],dtype=np.int32)
    
    #@POINTER(1)
    AQL_1 = np.array([AQL],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, AQL_1, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(2)
    LTFD_1 = np.array([LTFD],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, LTFD_1, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(3)
    PRDRISK_1 = np.array([PRDRISK],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, PRDRISK_1, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(4)
    CONRISK_1 = np.array([CONRISK],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, CONRISK_1, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(5)
    MINSMP_1 = np.array([MINSMP],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, MINSMP_1, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(6)
    MAXSMP_1 = np.array([MAXSMP],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, MAXSMP_1, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(7)
    NN = np.array([-1.0],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, NN, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(8)
    C = np.array([-1.0],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, C, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(9)
    Status = np.array([-1.0],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, Status, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #Run the script
    cScript = "SET ECHOIN 1 \n TAKE samsizr.lng \n GO \n QUIT \n"
    errorcode = lingo.pyLSexecuteScriptLng(pEnv, cScript)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #Close the log file
    errorcode = lingo.pyLScloseLogFileLng(pEnv)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    if Status[0] == lingo.LS_STATUS_GLOBAL_LNG:
        print("\nGlobal optimum found!")
    elif Status[0] == lingo.LS_STATUS_LOCAL_LNG:
        print("\nLocal optimum found!")
    else:
        print("\nSolution is non-optimal\n")

    #check solution
    print("\nThe Optimal sample size is ",NN,".\nAccept the lot if ",
           C," or less defectives in sample.\n\n")

    #delete Lingo enviroment object
    errorcode = lingo.pyLSdeleteEnvLng(pEnv)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        exit(1)

##############################################################################
if __name__ == '__main__':
    samsizr(0.03,0.08,0.09,0.05,125.0,400.0)
    sys.stdinp.read(1)


        
