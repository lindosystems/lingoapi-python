"""
The purpose of this sample is to test catching the different Lingo/Python API
 exceptions that can be raised by solve and the error callback function. 

"""
import lingo_api as lingo
import numpy as np


# Setting a default cbError function to catch any errors in 
# the shortestPath.lng script
uData = {}
# Callback solver 
def cbSolverInterrupt(pEnv, nReserved, uData): 
    return -1

def cbSolver(pEnv, nReserved, uData): 
    return 0

def cbError(pEnv, uData, nErrorCode, errorText):
    try:
        raise lingo.CallBackError(nErrorCode, errorText)
    except lingo.CallBackError as e:
        print("From Callback Error Function: ",e)
        exit(1)

"""
This model calls a callback function `cbSolverInterrupt` which returns -1 interrupting the model.
"""
def interruptedModel(lngFile):
    # Naming the set members
    TEST = np.array(["T1", "T2", "T3"])
    X    = np.zeros(len(TEST))
    # Create a model object
    model = lingo.Model(lngFile)
    # set all pointers in the order that they appear in chess.lng
    model.set_pointer("Pointer1",TEST,lingo.SET)
    model.set_pointer("Pointer2",X,lingo.VAR)

    # set the call back function and user data
    model.set_cbSolver(cbSolverInterrupt)
    model.set_cbError(cbError)
    model.set_uData(uData)
    return model

"""
This model does not assign data to the second pointer. A CallBackError will be raised followed by a LingoError.
"""
def missingPointerModel(lngFile):
    # Naming the set members
    TEST = np.array(["T1", "T2", "T3"])
    # Create a model object
    model = lingo.Model(lngFile)
    # set all pointers in the order that they appear in chess.lng
    model.set_pointer("Pointer1",TEST,lingo.SET)

    # set the call back function and user data
    model.set_cbSolver(cbSolver)
    model.set_cbError(cbError)
    model.set_uData(uData)
    return model

"""
The model returned by nonPointerTypeModel(lngFile) has a pointer with a type that does not exists. 
This model will cause solve() to raise PointerTypeNotSupportedError.
"""
def nonPointerTypeModel(lngFile):
    # Naming the set members
    TEST = np.array(["T1", "T2", "T3"])
    X    = np.zeros(len(TEST))
    # Create a model object
    model = lingo.Model(lngFile)
    # set all pointers in the order that they appear in chess.lng
    model.set_pointer("Pointer1",TEST,lingo.SET)
    model.set_pointer("Pointer2",X,5345)

    # set the call back function and user data
    model.set_cbSolver(cbSolver)
    model.set_cbError(cbError)
    model.set_uData(uData)
    return model

"""
The model returned by typeNotSupportedModel(lngFile) has pointer data that is not an allowed datatype.
This model will cause solve() to raise a TypeNotSupportedError exception.
"""
def typeNotSupportedModel(lngFile):
    # Naming the set members
    TEST = np.array(["T1", "T2", "T3"])
    X    = [0.0, 0.0, 0.0]
    # Create a model object
    model = lingo.Model(lngFile)
    # set all pointers in the order that they appear in chess.lng
    model.set_pointer("Pointer1",TEST,lingo.SET)
    model.set_pointer("Pointer2",X,lingo.VAR)

    # set the call back function and user data
    model.set_cbSolver(cbSolver)
    model.set_cbError(cbError)
    model.set_uData(uData)
    return model

"""
The model returned by emptyPointerModel(lngFile) has a pointer with an empty NumPy array. 
This model will cause solve() to raise the EmptyPointer exception. 
"""
def emptyPointerModel(lngFile):
    # Naming the set members
    TEST = np.array(["T1", "T2", "T3"])
    X    = np.array([])
    # Create a model object
    model = lingo.Model(lngFile)
    # set all pointers in the order that they appear in chess.lng
    model.set_pointer("Pointer1",TEST,lingo.SET)
    model.set_pointer("Pointer2",X,lingo.VAR)

    # set the call back function and user data
    model.set_cbSolver(cbSolver)
    model.set_cbError(cbError)
    model.set_uData(uData)
    return model

"""
run(model) prints the model then it calls solve wrapped in a try/except block.
"""
def run(model):  
    print(model)
    try:
        lingo.solve(model)
    except lingo.LingoError as err:
        if(err.error == 73):
            print(f"{lngFile} has been interrupted!")
        else:
            print(err)

    except lingo.TypeNotSupportedError as err:
        print(err)

    except lingo.EmptyPointer as err:
        print(err)
   
    except lingo.PointerTypeNotSupportedError as err:
        print(err)
    except Exception as err:
        print(err)
  

lngFile = "errorTest.lng"

print("\n","*"*60,"\n")

print("Testing a model that is interrupted: \n")
model = interruptedModel(lngFile)
run(model)
print("\n","*"*60,"\n")


print("Testing a model with a missing pointer: \n")
model = missingPointerModel(lngFile)
run(model)
print("\n","*"*60,"\n")


print("Testing a model with an invalid pointer type: \n")
model = nonPointerTypeModel(lngFile)
run(model)
print("\n","*"*60,"\n")


print("Testing a model with an invalid pointer data type: \n")
model = typeNotSupportedModel(lngFile)
run(model)
print("\n","*"*60,"\n")

print("Testing a model with an empty pointer: \n")
model = emptyPointerModel(lngFile)
run(model)
print("\n","*"*60,"\n")

