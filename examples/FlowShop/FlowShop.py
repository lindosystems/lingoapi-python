"""
Output:
Lingo API       Iteration: 30400 Objective: 25.0 Bound: 25.0
Machine: Blend
Sequence: B1->B2->B3->A1->A2->A3
Machine: Tablet
Sequence: B1->B2->B3->A1->A2->A3
"""

import lingo_api as lingo
import numpy as np
import pandas as pd

'''
cbError(pEnv, uData, nErrorCode, errorText)

LINGO API error callback

rasie an error when LINGO finds one
'''
def cbError(pEnv, uData, nErrorCode, errorText):
    raise lingo.CallBackError(nErrorCode, errorText)

'''
cbSolver(pEnv, nReserved, uData)

LINGO API callback.

prints out iteration, objective value and bound
'''
def cbSolver(pEnv, nReserved, uData):
    # allocate the numpy arrays for API callback getter functions
    nIters   = np.array([-1],dtype=np.int32)
    bestObj  = np.array([-1.0],dtype=np.double)
    objBound = np.array([-1.0],dtype=np.double)

    # Get the current iteration
    errorcode = lingo.pyLSgetIntCallbackInfoLng(pEnv, lingo.LS_IINFO_ITERATIONS_LNG, nIters)
    
    if nIters[0] > 0 and uData["LastIter"] < nIters[0] and nIters[0]%100 == 0:
        # Get the best objective value and the best objective bound
        errorcode = lingo.pyLSgetDouCallbackInfoLng(pEnv, lingo.LS_DINFO_MIP_BEST_OBJECTIVE_LNG, bestObj)
        errorcode = lingo.pyLSgetDouCallbackInfoLng(pEnv, lingo.LS_DINFO_MIP_BEST_OBJECTIVE_LNG, objBound)
        # update the LastIter saved in uData
        uData["LastIter"] = nIters[0]
        callbackStr = f"{uData['Prefix']:15} Iteration: {nIters[0]} Objective: {bestObj[0]} Bound: {objBound[0]}"
        print(callbackStr)
    return 0

'''
JobSequence(ZPred)

ZPred - 2d array of job sequence table for one machince
'''
# 
def JobSequence(ZPred):
# empty np array for job sequence
    JobSeq = np.empty(nJobs,dtype='object')

    # find the first job on diag
    firstJob = -1
    for i in range(0,nJobs):
        if(ZPred[i,i] == 1):
            firstJob = i
            break

    # with first job find the sequence
    curJob = firstJob
    JobSeq[0] = JOB[curJob]
    for i in range(1,nJobs):
    
        for j in range(0,nJobs):
            if(j != curJob and ZPred[curJob,j] == 1):
                curJob = j
                break
    
        JobSeq[i] = JOB[curJob]
    return JobSeq

lngFile = "FLowShopSeqX.lng"

blendDf = pd.read_csv('BlendData.csv', index_col=0)
tabletDf = pd.read_csv('TabletData.csv', index_col=0)

blendJobs = blendDf.axes[1]
tabletJobs = tabletDf.axes[1]



JOB = blendJobs
MACHINE = np.array(["Blend", "Tablet"])
nJobs = len(JOB)
nMach = len(MACHINE)

blendData = blendDf.to_numpy()
tabletData = tabletDf.to_numpy()

# Combine both DURN to make a DURN table
DURNBlend = blendData[0:1, :]
DURNTablet = tabletData[0:1, :]
DURN = np.array([DURNBlend,DURNTablet])


# Combine both Change Time tables to make an MxJxJ tabke
ChngTmBlend = blendData[1:, :]
ChngTmTablet = tabletData[1:, :]
ChngTm = np.array([ChngTmBlend,ChngTmTablet])

# Make arrays for output


STATUS = np.array([-1.0])
STIME = np.zeros((nMach,nJobs))
ZPRED = np.zeros((nMach,nJobs,nJobs))

"""
!API; JOB     = @POINTER( 1);
!API; MACHINE = @POINTER( 2);
!API; DURN    = @POINTER( 3);
!API; ChngTm  = @POINTER( 4);
!API; @POINTER(5) = STIME;
!API; @POINTER(6) = ZPRED;
!API; @POINTER(7) = @STATUS();
"""
# Create a model object
model = lingo.Model(lngFile)

# set all pointers in the order that they appear in TransportAPI.lng
model.set_pointer("Pointer1",JOB,lingo.SET)
model.set_pointer("Pointer2",MACHINE,lingo.SET)
model.set_pointer("Pointer3",DURN,lingo.PARAM)
model.set_pointer("Pointer4",ChngTm,lingo.PARAM)
model.set_pointer("Pointer5",STIME,lingo.VAR)
model.set_pointer("Pointer6",ZPRED,lingo.VAR)
model.set_pointer("Pointer7",STATUS,lingo.VAR)

# set the udata 
uData =  {"Prefix":"Lingo API", "LastIter":-1,}
# set the call back function and user data
model.set_cbError(cbError)
model.set_cbSolver(cbSolver)
model.set_uData(uData)
# now that everything is set call solve(model)
lingo.solve(model)


BlendSeq = JobSequence(ZPRED[0])
TabletSeq = JobSequence(ZPRED[1])


print(f"Machine: {MACHINE[0]}")
print(f"Sequence: {'->'.join(BlendSeq.tolist())}")


print(f"Machine: {MACHINE[1]}")
print(f"Sequence: {'->'.join(TabletSeq.tolist())}")