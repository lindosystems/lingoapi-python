"""
For our example, we will be cutting 45 foot wide rolls of paper into smaller rolls of widths: 34, 24, 15, 
10 and 18. We use Lingos programming capability to iteratively solve the master and subproblem 
until no further beneficial cutting patterns remain to be appended to the master problem.

Source: Lingo 19 User Manual

Input Files:
The Lingo file `loopCut.lng` is loaded from the same directory as this script, and 
contains the model.

Output: print out

Lingo API       Iteration:     5        Objective: 1019.0  Bound: 1019.0
Lingo API       Iteration:     6        Objective: 985.0  Bound: 985.0
Lingo API       Iteration:    10        Objective: 985.0  Bound: 985.0

Global optimum found!
Total raws used :   985.0
Total feet yield:   43121.0
Total feet used :   44325.0
Percent waste   :   2.7%

Name        Demand   Yield    Patterns:1-9
F34          350      350.0          1          0          0          0          1          0          0          0          0
F24          100      100.0          1          0          0          0          0          1          0          1          0
F15          800      801.0          1          0          3          0          0          0          1          0          1
F10         1001     1002.0          1          4          0          0          1          0          1          2          3
F18          377      377.0          1          0          0          2          0          1          1          0          0
Pattern:          1         2         3         4         5         6         7         8         9
Produce:        0.0       0.0     133.0       0.0     350.0     100.0     277.0       0.0     125.0

"""
import lingo_api as lingo
import numpy as np

uData =  {"Prefix":"Lingo API",
          "LastIter":-1,}

# Callback solver 
def cbSolver(pEnv, nReserved, uData):
    # allocate the numpy arrays for API callback getter functions
    nIters   = np.array([-1],dtype=np.int32)
    bestObj  = np.array([-1.0],dtype=np.double)
    objBound = np.array([-1.0],dtype=np.double)
    varName = np.array(["FINAL"],dtype="|S1024")
    val   = np.array([-1.0], dtype=np.double)

    # Variables do not show up right away this error code can be
    #  8 -> A variable name passed to LSgetCallbackVarPrimal() was invalid.
    #  5 -> A request was made for information that is not currently available.
    # before eventual being 0
    # check errors while debugging 
    # if errorcode != lingo.LSERR_NO_ERROR_LNG:
    #     raise lingo.LingoError(errorcode)
    errorcode = lingo.pyLSgetCallbackVarPrimalLng(pEnv, varName, val)
    # Gets the current iteration
    errorcode = lingo.pyLSgetIntCallbackInfoLng(pEnv, lingo.LS_IINFO_ITERATIONS_LNG, nIters)
    
    # if the master/integer problem is being solved and the current iteration has not 
    # been passed to the callback then print out the progress
    if val[0] == 1 and nIters[0] > 0 and uData["LastIter"] < nIters[0]:
        # Get the best objective value and the best objective bound
        errorcode = lingo.pyLSgetDouCallbackInfoLng(pEnv, lingo.LS_DINFO_MIP_BEST_OBJECTIVE_LNG, bestObj)
        errorcode = lingo.pyLSgetDouCallbackInfoLng(pEnv, lingo.LS_DINFO_MIP_BEST_OBJECTIVE_LNG, objBound)
        # update the LastIter saved in uData
        uData["LastIter"] = nIters[0]
        callbackStr = f"{uData['Prefix']:15} Iteration: {nIters[0]:5}\
        Objective: {bestObj[0]:5}  Bound: {objBound[0]:5}"
        print(callbackStr)
    return 0

def cbError(pEnv, uData, nErrorCode, errorText):
    # A exception will be displayed if this callback is called
    raise lingo.CallBackError(nErrorCode, errorText)


lngFile = "loopCut.lng"

# Model Data
FG = np.array(["F34","F24","F15","F10","F18"])
WIDTH = np.array([34, 24, 15, 10, 18])
DEM = np.array([350, 100, 800, 1001, 377])
NPATTERNS = 20
RMWIDTH = 45
NFG = len(FG)

# Return Data
X = np.zeros(NPATTERNS)
NPATS = np.array([-1.0])
NBR = np.zeros(NFG*NPATTERNS)
STATUS = np.array([-1.0])

pointerDict = {"Pointer1":NPATTERNS,
               "Pointer2":FG, 
               "Pointer3":WIDTH, 
               "Pointer4":DEM, 
               "Pointer5":RMWIDTH,
               "Pointer6":X,
               "Pointer7":NPATS,
               "Pointer8":NBR,
               "Pointer9":STATUS
               }

model = lingo.Model(lngFile , pointerDict, "log")

model.set_cbSolver(cbSolver)
model.set_cbError(cbError)
model.set_uData(uData)

lingo.solve(model)

if STATUS[0] == lingo.LS_STATUS_GLOBAL_LNG:
    print("\nGlobal optimum found!")
elif STATUS[0] == lingo.LS_STATUS_LOCAL_LNG:
    print("\nLocal optimum found!")
else:
    print("\nSolution is non-optimal\n")


# Resahpe the data for calculation 
# or to save data in a csv
NPATS = int(NPATS[0])
NBR   = np.reshape(NBR, (NFG, NPATTERNS))
WIDTH = np.reshape(WIDTH, (NFG, 1))
DEM   = np.reshape(DEM, (NFG, 1))
FG    = np.reshape(FG, (NFG, 1))
# Compute the output data
X         = np.reshape(X, (1, NPATTERNS))
rawUsed  = np.sum(X)
totalRaw = np.ceil(rawUsed/RMWIDTH) * RMWIDTH
Yield    = np.sum(X*NBR, axis=1, keepdims=True)

totalUsed    = rawUsed * RMWIDTH 
totalYield   = np.sum(X*NBR*WIDTH)
wastePercent = (1 - totalYield/totalUsed )* 100

# Sample Output
print(f"Total raws used :   {rawUsed}")
print(f"Total feet yield:   {totalYield}")
print(f"Total feet used :   {totalUsed}")
print(f"Percent waste   :   {wastePercent:.1f}%")
print()
print(f"Name        Demand   Yield    Patterns:{1}-{NPATS}")
for i in range(0,NFG):
    pStr = f"{FG[i][0]:5} {DEM[i][0]:10} {Yield[i][0]:10} "
    for j in range(0,NPATS):
        pStr += f"{int(NBR[i,j]):10} "
    print(pStr)

enumStr = "Pattern: "
pStr    = "Produce: "
for i in range(0,NPATS):
    enumStr += f"{i+1:10}"
    pStr    += f"{X[0][i]:10}"
print(enumStr)
print(pStr)