"""
Transport API Demo

"""


import lingo_api as lingo
import numpy as np

# Setting a default cbError function to catch any errors in 
uData = {}
def cbError(pEnv, uData, nErrorCode, errorText):
    raise lingo.CallBackError(nErrorCode, errorText)



lngFile = "TransportAPI.lng"

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

SUPPLIER = np.array(["SUP1", "SUP2", "SUP3"])
CAPACITY = np.array([60, 55, 51])
CUSTOMER = np.array(["CUST1", "CUST2", "CUST3", "CUST4"])
DEMAND   = np.array([35, 37, 22, 32])
COST     =  np.array( [[6, 2, 6, 7],                                                    
                       [4, 9, 5, 3],
                       [5, 2, 1, 9]])  

nSup = SUPPLIER.shape[0]
nCust = CUSTOMER.shape[0]
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

# set all pointers in the order that they appear in chess.lng
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
model.set_uData(uData)
# now that everything is set call solve(model)
lingo.solve(model)


# check that the model has ben solved 
if STATUS == lingo.LS_STATUS_GLOBAL_LNG:
    print("\nGlobal optimum found!")
elif STATUS == lingo.LS_STATUS_LOCAL_LNG:
    print("\nLocal optimum found!")
else:
    print(f"\nSolution is non-optimal Status Code: %d\n", STATUS[0])

# shape flow using order F for FORTRAN
FLO, ptrType   = model.get_pointer("Pointer6")
print(FLO)

# now display the results 
print(f"Total Cost: {TransCost[0]}\n")
for i in range(0, nCust):
    print(f"{CUSTOMER[i]} Demand {DEMAND[i]}")
    tempTotal = 0
    for j in range(0, nSup):
        tempTotal += FLO[j,i]
        print(f"\t{SUPPLIER[j]}: {FLO[j,i]}")
    
    print(f"\tTotal: {tempTotal}\n")



