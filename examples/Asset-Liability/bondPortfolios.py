"""

Dedicated Bond Portfolio.
This is a linear model that minimizes the cost of a bond portfolio whose cashflows 
match a given steam of liabilities. It is assumed that any surplus cash is carried from 
one year to the next with no interest earned 

Immunized Bond Portfolio.
This is a linear model that minimizes the cost of a bond portfolio whose present value,
dollar duration, and dollar convexity matches the liability streams.

Source: Gerard Cornuejols `Optimization Methods in Finance`

The sample requires two additional libraries pandas and matplotlib

Input:
The Lingo file `dedicatedPortfolio.lng` and `immunized.lng` is loaded from the same directory as this script, and 
contains the model.
The first csv file is `bondData.csv`, and includes the bond names, price, and the cash flows. 
The second csv file is `libilities.csv` and includes the liability stream and risk-free rate of return.
Both csv files by default it is in the same directory as this script.


Output:
Bond               Dedicated Portfolio    Immunized Portfolio
                         Amount                Amount
================================================================
Bond 1                   0.0000                0.0000
Bond 2                   0.0000                0.0000
Bond 3                  11.1111               15.4453
Bond 4                   0.0000                0.0000
Bond 5                   6.6459                0.0000
Bond 6                   0.6093                0.0000
Bond 7                   0.0000                0.0000
Bond 8                   0.0000                0.0000
Bond 9                   6.1198                7.2119
Bond 10                  0.0000                0.0000
Bond 11                  0.1089                4.3428
Bond 12                  0.0000                0.0000
Bond 13                  3.1089                0.0000
================================================================
Cost                     2754.2845       2751.5223
Preaent Value            2757.9368       2757.9368
Dollar Duration          9863.2116       9863.2116
Duration Convexity      52066.8050      52066.8050


A plot of the yield curve is saved by default to the current working directory.
Finally, a `dedicatedPortfolio.log` is saved to the working directory and has the model, and output.
This log file is very useful for debugging any changes.

"""

import lingo_api as lingo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

uData = {}
def cbError(pEnv, uData, nErrorCode, errorText):
    raise lingo.CallBackError(nErrorCode, errorText)

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



lngDedicatedFile = "dedicatedPortfolio.lng"
logDedicatedFile = "dedicatedPortfolio.log"

lngImmunizedFile = "immunized.lng"
logImmunizedFile = "immunized.log"

# Load
bondDf = pd.read_csv("bondData.csv")
liabilitiesDf = pd.read_csv("liabilities.csv")

# Prepare bond data
BONDS   = bondDf.Bond_Name.values 
PRICE  = bondDf.Price.values
NUM_BONDS = len(BONDS)
bondDataStarts = 2
CASH_FLOWS   = bondDf.iloc[:,bondDataStarts:].values
timeLabel = bondDf.iloc[:,bondDataStarts:].columns
# Liability stream and risk free returns
LIABILITIES = liabilitiesDf.liability.values
NUM_LIABILITIES = len(LIABILITIES)
riskFree    = liabilitiesDf.RiskFree.values
t = np.arange(1,NUM_LIABILITIES + 1, dtype=int)
# Need PV_L DD_L DC_L then PV DD DC of each bond
PV_L = (PV(LIABILITIES,riskFree,t))
DD_L = (DD(LIABILITIES,riskFree,t))
DC_L = (DC(LIABILITIES,riskFree,t))
PV_B = np.array([PV(CASH_FLOWS[i], riskFree, t) for i in range(0,NUM_BONDS)])
DD_B = np.array([DD(CASH_FLOWS[i], riskFree, t) for i in range(0,NUM_BONDS)])
DC_B = np.array([DC(CASH_FLOWS[i], riskFree, t) for i in range(0,NUM_BONDS)])


DEDICATE_AMOUNT = np.zeros(NUM_BONDS)
IMMUNIZED_AMOUNT = np.zeros(NUM_BONDS)
DUAL_PRICE = np.zeros(NUM_LIABILITIES)

DEDICATE_STATUS  = -1
IMMUNIZED_STATUS = -1

dedicatedPointerDict = {"Pointer1":NUM_LIABILITIES,
                        "Pointer2":BONDS,
                        "Pointer3":PRICE,
                        "Pointer4":LIABILITIES,
                        "Pointer5":CASH_FLOWS,
                        "Pointer6":DEDICATE_AMOUNT,
                        "Pointer7":DUAL_PRICE,
                        "Pointer8":DEDICATE_STATUS
}

immunizedPointerDict = {"Pointer1":BONDS,
                        "Pointer2":PRICE,
                        "Pointer3":PV_B,
                        "Pointer4":DD_B,
                        "Pointer5":DC_B,
                        "Pointer6":PV_L,
                        "Pointer7":DD_L,
                        "Pointer8":DC_L,
                        "Pointer9":IMMUNIZED_AMOUNT,
                        "Pointer10":IMMUNIZED_STATUS
}

dedicatedModel = lingo.Model(lngDedicatedFile, dedicatedPointerDict, logDedicatedFile)
immunizedModel = lingo.Model(lngImmunizedFile, immunizedPointerDict, logImmunizedFile)

dedicatedModel.set_cbError(cbError)
dedicatedModel.set_uData(uData)
immunizedModel.set_cbError(cbError)
immunizedModel.set_uData(uData)

lingo.solve(dedicatedModel)
lingo.solve(immunizedModel)


dedicated_cost = np.sum(DEDICATE_AMOUNT*PRICE)
dedicated_PV   = np.sum(DEDICATE_AMOUNT*PV_B)
dedicated_DD   = np.sum(DEDICATE_AMOUNT*DD_B)
dedicated_DC   = np.sum(DEDICATE_AMOUNT*DC_B)


immunized_cost = np.sum(IMMUNIZED_AMOUNT*PRICE)
immunized_PV   = np.sum(IMMUNIZED_AMOUNT*PV_B)
immunized_DD   = np.sum(IMMUNIZED_AMOUNT*DD_B)
immunized_DC   = np.sum(IMMUNIZED_AMOUNT*DC_B)

DEDICATE_STATUS = dedicatedModel.get_pointer("Pointer8")
IMMUNIZED_STATUS = immunizedModel.get_pointer("Pointer10")

if DEDICATE_STATUS == lingo.LS_STATUS_GLOBAL_LNG:
    print("Dedicated portfolio: Global optimum found!")
elif DEDICATE_STATUS == lingo.LS_STATUS_LOCAL_LNG:
    print("Dedicated portfolio: Local optimum found!")
else:
    print("Dedicated portfolio: Solution is non-optimal")

if IMMUNIZED_STATUS == lingo.LS_STATUS_GLOBAL_LNG:
    print("Immunized portfolio: Global optimum found!")
elif IMMUNIZED_STATUS == lingo.LS_STATUS_LOCAL_LNG:
    print("Immunized portfolio: Local optimum found!")
else:
    print("Immunized portfolio: Solution is non-optimal")


print(f"Bond               Dedicated Portfolio    Immunized Portfolio")
print(f"                         Amount                Amount")
print("================================================================")
for i in range(0,NUM_BONDS):
    print(f"{BONDS[i]:10} {DEDICATE_AMOUNT[i]:20.4F}  {IMMUNIZED_AMOUNT[i]:20.4F} ")
print("================================================================")
print(f"{'Cost              ':10} {dedicated_cost:15.4f} {immunized_cost:15.4f}")
print(f"{'Preaent Value     ':10} {dedicated_PV:15.4f} {immunized_PV:15.4f}")
print(f"{'Dollar Duration   ':10} {dedicated_DD:15.4f} {immunized_DD:15.4f}")
print(f"{'Duration Convexity':10} {dedicated_DC:15.4f} {immunized_DC:15.4f}")



spotRate = np.fromiter( (1/DUAL_PRICE[i]**(1/(i+1)) - 1 for i in range(0,len(DUAL_PRICE))), dtype=np.double)

plt.plot(timeLabel, spotRate)
plt.plot(timeLabel, riskFree)
plt.legend(["Dedicated Portfolio", "Risk Free"])
plt.title("Yeild Curve")
plt.xlabel("time to maturity")
plt.ylabel("yield")
plt.savefig('yeildCurve.png')



