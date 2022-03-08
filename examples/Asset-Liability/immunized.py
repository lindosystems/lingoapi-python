"""
Immunized Bond Portfolio.
This is a linear model that minimizes the cost of a bond portfolio whose present value,
dollar duration, and dollar convexity matches the liability streams.
Source: Gerard Cornuejols `Optimization Methods in Finance`

The sample requires the pandas library

Input: 
The Lingo file `immunized.lng` is loaded from the same directory as this script, and 
contains the model.
The first csv file is `bondData.csv`, and includes the bond names, price, and the cash flows. 
The second csv file is `libilities.csv` and includes the liability stream and risk free rate of return.
Both csv files by default it is in the same directory as this script.

Output:
The total cost of the liabilities, its present value, and the cost of the portfolio.
Also, a data frame displays the amount of each bond to purchase.  
Finally, a `immunized.log` is saved to the working directory and has the model, and output.
This log file is very useful for debugging any changes.

"""

import lingo_api as lingo
import pandas as pd
import numpy as np

def lingoModel(bondPrices, PV_L, DD_L, DC_L, PV_B, DD_B, DC_B):

    #create Lingo enviroment object
    pEnv = lingo.pyLScreateEnvLng()
    if pEnv is None:
        print("cannot create LINGO environment!")
        exit(1)

    #open LINGO's log file
    errorcode = lingo.pyLSopenLogFileLng(pEnv,'immunized.log')
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #pass memory transfer pointers to LINGO
    #define pnPointersNow
    pnPointersNow = np.array([0],dtype=np.int32)

    #@POINTER( 1) number of bonds 
    numBonds = len(bondPrices)
    numBondsArry = np.array([numBonds], dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, numBondsArry, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 2) bond prices 
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, bondPrices, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 3) bond prices 
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, PV_B, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 4) bond prices 
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, DD_B, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 5) bond prices 
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, DC_B, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER( 6) bond prices 
    PV_Larray = np.array([PV_L], dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, PV_Larray, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER( 7) bond prices 
    DD_Larray = np.array([DD_L], dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, DD_Larray, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER( 8) bond prices 
    DC_Larray = np.array([DC_L], dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, DC_Larray, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 9) gets bond amounts
    amount = np.empty((numBonds), dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, amount, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(10)
    Status = np.array([-1.0],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, Status, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #Run the script
    cScript = "SET ECHOIN 1 \n TAKE immunized.lng \n GO \n QUIT \n"
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

    #delete Lingo enviroment object
    errorcode = lingo.pyLSdeleteEnvLng(pEnv)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        exit(1)

    return amount
# Compute the presentvalue of cashflow
def PV(L,rf,t):
    PV = np.sum(L/(1+rf)**t, axis=0)
    return PV
# Compute Fisher-Weil dollar duration
def DD(L,rf,t):
    DD = np.sum(t*L/(1+rf)**(t+1))
    return DD
# Compute the dollar convexity
def DC(L,rf,t):
    DC = np.sum(t*(t+1)*L/(1+rf)**(t+2))
    return DC

def main():
    # Load data 
    bondDf = pd.read_csv("bondData.csv")
    liabilitiesDf = pd.read_csv("liabilities.csv")
    # Prepare bond data
    bondNames   = bondDf.Bond_Name.values
    bondPrices  = bondDf.Price.values.astype(np.double)
    nBonds = len(bondNames)
    bondDataStarts = 2
    cashFLows   = bondDf.iloc[:,bondDataStarts:].values.astype(np.double)
    # Liability stream and risk free returns
    liabilities = liabilitiesDf.liability.values
    riskFree    = liabilitiesDf.RiskFree.values
    nLiabilities = len(liabilities)
    t = np.arange(1,nLiabilities + 1, dtype=int) 
    # Need PV_L DD_L DC_L then PV DD DC of each bond
    PV_L = PV(liabilities,riskFree,t)
    DD_L = DD(liabilities,riskFree,t)
    DC_L = DC(liabilities,riskFree,t)
    PV_B = np.array([PV(cashFLows[i], riskFree, t) for i in range(0,nBonds)], dtype=np.double)
    DD_B = np.array([DD(cashFLows[i], riskFree, t) for i in range(0,nBonds)], dtype=np.double)
    DC_B = np.array([DC(cashFLows[i], riskFree, t) for i in range(0,nBonds)], dtype=np.double)
    amount = lingoModel(bondPrices, PV_L, DD_L, DC_L, PV_B, DD_B, DC_B)
    # make portfolio table
    numCols = len(bondNames)
    bondNames = np.reshape(bondNames,(numCols))
    amount = np.reshape(amount,(1,numCols))
    portfolioCost = np.dot(amount,bondPrices)[0]
    totalLiabilities = np.sum(liabilities)
    portfolioDf = pd.DataFrame(data=amount, index=["Amount"], columns=bondNames)
    print("Total Libilities            : $", totalLiabilities)
    print("Present Value of Libilities : $", PV_L)
    print("Portfolio Cost              : $", portfolioCost)
    print(portfolioDf)
    return 0
    
if __name__ == '__main__':
    main()

    