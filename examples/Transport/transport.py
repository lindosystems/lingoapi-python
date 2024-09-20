"""
Transport API Demo

Lingo API       Iteration: 5  Objective: 344.0

Global optimum found!
Total Cost: 344.0

CUST1 Demand 35
        SUP1: 0.0
        SUP2: 23.0
        SUP3: 12.0
        Total: 35.0

CUST2 Demand 37
        SUP1: 37.0
        SUP2: 0.0
        SUP3: 0.0
        Total: 37.0

CUST3 Demand 22
        SUP1: 0.0
        SUP2: 0.0
        SUP3: 22.0
        Total: 22.0

CUST4 Demand 32
        SUP1: 0.0
        SUP2: 32.0
        SUP3: 0.0
        Total: 32.0

"""


import lingo_api as lingo
import numpy as np
import pandas as pd

uData =  {"Prefix":"Lingo API", "LastIter":-1,}
# Setting a default cbError function to catch any errors in 
def cbError(pEnv, uData, nErrorCode, errorText):
    raise lingo.CallBackError(nErrorCode, errorText)

# Callback solver 
def cbSolver(pEnv, nReserved, uData):
    # allocate the numpy arrays for API callback getter functions
    nIters   = np.array([-1],dtype=np.int32)
    bestObj  = np.array([-1.0],dtype=np.double)

    # Get the current iteration
    errorcode = lingo.pyLSgetIntCallbackInfoLng(pEnv, lingo.LS_IINFO_ITERATIONS_LNG, nIters)
    
    if nIters[0] > 0 and uData["LastIter"] < nIters[0]:
        # Get the best objective value
        errorcode = lingo.pyLSgetDouCallbackInfoLng(pEnv, lingo.LS_DINFO_OBJECTIVE_LNG, bestObj)
        # update the LastIter saved in uData
        uData["LastIter"] = nIters[0]
        callbackStr = f"{uData['Prefix']:15} Iteration: {nIters[0]}\
                          Objective: {bestObj[0]}"
        print(callbackStr)
    return 0


lngFile = "TransportAPI.lng"
# CSV:
# Set to True to read data from Cost_Cap_Dem.csv
# Set to False to read data from this script
CSV = True
"""
 ! Sample data from LINGO; 
   SUPPLIER = SUP1 SUP2 SUP3 ;  
   CAPACITY =  60   55   51 ; 
   CUSTOMER = CUST1 CUST2 CUST3 CUST4 ;
   DEMAND =    35     37    22   32 ;
   COST =       6      2     6    7  
                4      9     5    3 
                5      2     1    9 ;
"""

if CSV:
    df = pd.read_csv('Cost_Cap_Dem.csv', index_col=0)
    data = df.to_numpy()
    SUPPLIER = df.axes[0][0:-1]
    CAPACITY = data[0:-1,-1]
    CUSTOMER = df.axes[1][0:-1]
    DEMAND   = data[-1,0:-1]
    COST     = data[0:-1, 0:-1]
else:
    SUPPLIER = np.array(["SUP1", "SUP2", "SUP3"])
    CAPACITY = np.array([60, 55, 51])
    CUSTOMER = np.array(["CUST1", "CUST2", "CUST3", "CUST4"])
    DEMAND   = np.array([35, 37, 22, 32])
    COST     =  np.array( [[6, 2, 6, 7],                                                    
                          [4, 9, 5, 3],
                         [5, 2, 1, 9]])  

nSup = len(SUPPLIER)
nCust = len(CUSTOMER)
FLO = np.zeros((nSup,nCust))
TransCost = np.array([-1.0])
STATUS = np.array([-1.0])

"""
   @POINTER(1) = SUPPLIER;
   @POINTER(2) = CAPACITY;
   @POINTER(3) = CUSTOMER;
   @POINTER(4) = DEMAND;
   @POINTER(5) = COST;
   @POINTER(6) = FLO;
   @POINTER(7) = TransCost;
   @POINTER(8) = @STATUS();
"""

# Create a model object
model = lingo.Model(lngFile)

# set all pointers in the order that they appear in TransportAPI.lng
model.set_pointer("Pointer1",SUPPLIER,lingo.SET)
model.set_pointer("Pointer2",CAPACITY,lingo.PARAM)
model.set_pointer("Pointer3",CUSTOMER,lingo.SET)
model.set_pointer("Pointer4",DEMAND,lingo.PARAM)
model.set_pointer("Pointer5",COST,lingo.PARAM)
model.set_pointer("Pointer6",FLO,lingo.VAR)
model.set_pointer("Pointer7",TransCost,lingo.VAR)
model.set_pointer("Pointer8",STATUS,lingo.VAR)

# set the call back function and user data
model.set_cbError(cbError)
model.set_cbSolver(cbSolver)
model.set_uData(uData)
# now that everything is set call solve(model)
lingo.solve(model)


# check that the model has ben solved 
#STATUS, ptrType   = model.get_pointer("Pointer8")
if STATUS == lingo.LS_STATUS_GLOBAL_LNG:
    print("\nGlobal optimum found!")
elif STATUS == lingo.LS_STATUS_LOCAL_LNG:
    print("\nLocal optimum found!")
else:
    print(f"\nSolution is non-optimal Status Code: %d\n", STATUS[0])

#FLO, ptrType   = model.get_pointer("Pointer6")
#TransCost, ptrType   = model.get_pointer("Pointer7")

# now display the results 
print(f"Total Cost: {TransCost[0]}\n")
for i in range(0, nCust):
    print(f"{CUSTOMER[i]} Demand {DEMAND[i]}")
    tempTotal = 0
    for j in range(0, nSup):
        tempTotal += FLO[j,i]
        print(f"\t{SUPPLIER[j]}: {FLO[j,i]}")
    
    print(f"\tTotal: {tempTotal}\n")



