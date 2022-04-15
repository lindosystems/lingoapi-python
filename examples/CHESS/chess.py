"""
In blending problems, two or more raw materials are to be blended into one or more 
finished goods, satisfying one or more quality requirements on the finished goods.
In this example, the Chess Snackfoods Co. markets four brands of mixed nuts. 
Each brand contains a specified ration of peanuts and cashews. 
Chess has contracts with suppliers to receive 750 pounds of peanuts/day and 250 
pounds of cashews/day. The problem is to determine the number of pounds of each brand
to produce each day to maximize total revenue without exceeding the available supply
of nuts.

max p'x
st Fx <= b
x >= 0

p - price that each brand sells for
F - formula matrix F_ij number of nut_i needed in brand_j
b - supply of each type of nut
x - amount of each brand to produce


Input Files:
The Lingo file `chess.lng` is loaded from the same directory as this script, and 
contains the model.

Output: print out

Global optimum found!
Brand      Peanut       Cashew     Produce
==========================================
Pawn         721.1538    48.0769   769.2308
Knight         0.0000     0.0000     0.0000
Bishop         0.0000     0.0000     0.0000
King          28.8462   201.9231   230.7692
==========================================
Totals          750.0      250.0     1000.0

"""

import lingo_api as lingo
import numpy as np


uData = {}
def cbError(pEnv, uData, nErrorCode, errorText):
    raise lingo.CallBackError(nErrorCode, errorText)

lngFile = "chess.lng"

NUTS   = np.array(["Peanut","Cashew"])
BRANDS = np.array(["Pawn", "Knight", "Bishop", "King"])   
SUPPLY     =  np.array( [750, 250])          # Total supply of each type
PRICE      =  np.array( [2,3,4,5])           # price that each brand charge
FORMULA    =  np.array( [[15,10, 6, 2],                                                    
                            [1, 6,10,14]])      # formula matrix 
peanut_i   = 0
cashew_i   = 1
PRODUCE    = np.zeros(len(PRICE))
STATUS     = -1

NUT_COUNT   = len(SUPPLY)
BRAND_COUNT = len(PRICE)





pointerDict = {"Pointer1":NUTS,
               "Pointer2":BRANDS, 
               "Pointer3":SUPPLY, 
               "Pointer4":PRICE, 
               "Pointer5":FORMULA,
               "Pointer6":PRODUCE, 
               "Pointer7":STATUS
               }


model = lingo.Model(lngFile , pointerDict,"log")

model.set_cbError(cbError)
model.set_uData(uData)

lingo.solve(model)

STATUS  = model.get_pointer("Pointer7")
PRODUCE = model.get_pointer("Pointer6")


if STATUS == lingo.LS_STATUS_GLOBAL_LNG:
    print("\nGlobal optimum found!")
elif STATUS == lingo.LS_STATUS_LOCAL_LNG:
    print("\nLocal optimum found!")
else:
    print("\nSolution is non-optimal\n")

totalPeanuts = np.sum(PRODUCE*FORMULA[peanut_i]/16)
totalCashew  = np.sum(PRODUCE*FORMULA[cashew_i]/16)
totalProduced = np.sum(PRODUCE)
print(f"Brand      Peanut       Cashew     Produce")
print(f"==========================================")
for i in range(0,BRAND_COUNT):
    peanuts = PRODUCE[i]*FORMULA[peanut_i,i]/16
    cashews = PRODUCE[i]*FORMULA[cashew_i,i]/16
    print(f"{BRANDS[i]:10} {peanuts:10.4f} {cashews:10.4f} {PRODUCE[i]:10.4f}")
print(f"==========================================")
print(f"{'Totals':10} {totalPeanuts:10} {totalCashew:10} {totalProduced:10}")
