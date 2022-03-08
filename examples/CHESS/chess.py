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

The sample requires one additional library pandas for data frames.

Input Files:
The Lingo file `chess.lng` is loaded from the same directory as this script, and 
contains the model. Finally model data can be entered in main().

Output:
A data frame is displayed the brand names, the nut mixture, and the amount to produce.
Finally, a `chess.log` is saved to the working directory and has the model, and output.
This log file is very useful for debugging any changes.

"""
import lingo_api as lingo
import numpy
import pandas as pd

def chess(nutSupply, price, formula):

    #create Lingo enviroment object
    pEnv = lingo.pyLScreateEnvLng()
    if pEnv is None:
        print("cannot create LINGO environment!")
        exit(1)

    #open LINGO's log file
    errorcode = lingo.pyLSopenLogFileLng(pEnv,'chess.log')
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #pass memory transfer pointers to LINGO
    #define pnPointersNow
    pnPointersNow = numpy.array([0],dtype=numpy.int32)

    #@POINTER(1)
    nutCount = len(nutSupply)
    nutCountArray = numpy.array( [nutCount],dtype=numpy.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, nutCountArray, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER(2)
    brandCount = len(price)
    brandCountArray = numpy.array( [brandCount],dtype=numpy.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, brandCountArray, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(3)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, nutSupply, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER(4)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, price, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #@POINTER(5)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, formula.flatten(), pnPointersNow)   # Flatten matrix into vector
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    
    #@POINTER(6)
    produce = numpy.ones((brandCount), dtype=numpy.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, produce, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)
    produce = numpy.reshape(produce,(1,brandCount))

    #@POINTER(7)
    Status = numpy.array([-1.0],dtype=numpy.double)
    errorcode = lingo.pyLSsetDouPointerLng(pEnv, Status, pnPointersNow)
    if errorcode != lingo.LSERR_NO_ERROR_LNG:
        print("errorcode = ", errorcode)
        exit(1)

    #Run the script
    cScript = "SET ECHOIN 1 \n TAKE chess.lng \n GO \n QUIT \n"
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

    return produce

def main():

    nutSupply  =  numpy.array( [750, 250],dtype=numpy.double)          # Total supply of each type
    price      =  numpy.array( [2,3,4,5],dtype=numpy.double)           # price that each brand charges
    formula    =  numpy.array( [[15,10, 6, 2],                                                    
                                [1, 6,10,14]], dtype=numpy.double)     # formula matrix 
    brandNames = numpy.array(["Pawn", "Knight", "Bishopp", "King"])    
    nutType    = numpy.array(["Peanut", "Cashew"])
    produce = chess(nutSupply, price, formula)

    # Pandas data frames for supplied model data and results from running the data
    modelData  = pd.DataFrame(data=formula, index=nutType, columns=brandNames, dtype=(numpy.int64, numpy.int64))
    resultData = pd.DataFrame(data=produce, index=["produce"], columns=brandNames)
    # Combine the two for a print out or make a csv 
    df = modelData.append(resultData)
    print(df)
    return 0

main()