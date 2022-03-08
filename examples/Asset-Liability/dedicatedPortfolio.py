"""

Dedicated Bond Portfolio.
This is a linear model that minimizes the cost of a bond portfolio whose cashflows 
match a given steam of liabilities. It is assumed that any surplus cash is carried from 
one year to the next with no interest earned 
Source: Gerard Cornuejols `Optimization Methods in Finance`

The sample requires two additional libraries pandas and matplotlib

Input:
The Lingo file `dedicatedPortfolio.lng` is loaded from the same directory as this script, and 
contains the model.
The first csv file is `bondData.csv`, and includes the bond names, price, and the cash flows. 
The second csv file is `libilities.csv` and includes the liability stream and risk-free rate of return.
Both csv files by default it is in the same directory as this script.

Output:
Two data frames displaying first the optimal portfolio and second the term structure of interest rates.
A plot of the yield curve is saved by default to the current working directory.
Finally, a `dedicatedPortfolio.log` is saved to the working directory and has the model, and output.
This log file is very useful for debugging any changes.

"""

import lingo_api as lingo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def lingoModel(bondPrices, cashFLows, liabilities):

    #create Lingo enviroment object
    pEnv = lingo.pyLScreateEnvLng()
    if pEnv is None:
        print("cannot create LINGO environment!")
        exit(1)

    #open LINGO's log file
    errorcode = lingo.pyLSopenLogFileLng(pEnv,'dedicatedBondPortfolio.log')
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

    #@POINTER( 2) number of liabilities 
    numLiabilities = len(liabilities)
    numLiabilitiesArry = np.array([numLiabilities], dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, numLiabilitiesArry, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 3) bond prices 
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, bondPrices, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 4) liability stream 
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, liabilities, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER( 5) cash fLow matrix
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, cashFLows.flatten(), pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 6) gets bond amounts
    amount = np.empty((numBonds), dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, amount, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER( 7) Get the dual pointers
    duals = np.empty((numLiabilities), dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, duals, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER( 8)
    Status = np.array([-1.0],dtype=np.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, Status, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #Run the script
    cScript = "SET ECHOIN 1 \n TAKE dedicatedPortfolio.lng \n GO \n QUIT \n"
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

    return amount, duals

def main():
    # Load
    bondDf = pd.read_csv("bondData.csv")
    liabilitiesDf = pd.read_csv("liabilities.csv")
    # Prepare bond data
    bondNames   = bondDf.Bond_Name.values
    bondPrices  = bondDf.Price.values.astype(np.double)
    bondDataStarts = 2
    cashFLows   = bondDf.iloc[:,bondDataStarts:].values.astype(np.double)
    timeLabel = bondDf.iloc[:,bondDataStarts:].columns
    # Liability stream and risk free returns
    liabilities = liabilitiesDf.liability.values.astype(np.double)
    riskFree    = liabilitiesDf.RiskFree.values.astype(np.double)
    # Run model
    amount, duals = lingoModel(bondPrices, cashFLows, liabilities)
    # Compute spot rate from duals
    spotRate = np.fromiter( (1/duals[i]**(1/(i+1)) - 1 for i in range(0,len(duals))), dtype=np.double)
    # make portfolio table
    numCols = len(bondNames)
    bondNames = np.reshape(bondNames,(numCols))
    amount = np.reshape(amount,(1,numCols))
    portfolioDf = pd.DataFrame(data=amount, index=["Amount"], columns=bondNames)
    # make spot rate and discount factor table
    df = pd.DataFrame(data=[spotRate,duals], index=["Spot Rate", "Discount Factor"], columns=timeLabel)
    portfolioCost = np.dot(amount,bondPrices)[0]
    totalLiabilities = np.sum(liabilities)
    portfolioDf = pd.DataFrame(data=amount, index=["Amount"], columns=bondNames)
    print("Total Libilities            : $", totalLiabilities)
    # print("Present Value of Libilities : $", PV_L)
    print("Portfolio Cost              : $", portfolioCost)
    print(portfolioDf)
    print(df)
    plt.plot(timeLabel, spotRate)
    plt.plot(timeLabel, riskFree)
    plt.legend(["Portfolio", "Risk Free"])
    plt.title("Yeild Curve")
    plt.xlabel("time to maturity")
    plt.ylabel("yield")
    plt.savefig('yeildCurve.png')
    
    return 0


if __name__ == '__main__':
    main()