"""
    Shortest Path a network example.
    This network LP finds the shortest path from source to sink through a directed graph.

    Input:
    The Lingo file `shortestPath.lng` is loaded from the same directory as this script, and 
    contains the model. The network data is stored in network.csv and is read in with 
    the pandas library. 
    Output:
    Global optimum found!
    Cost:  3.0
    Shortest Path: 1 -> 2 -> 4 -> 6

"""
import lingo_api as lingo
import numpy as np
import pandas as pd

# Setting a default cbError function to catch any errors in 
# the shortestPath.lng script
uData = {}
def cbError(pEnv, uData, nErrorCode, errorText):
    raise lingo.CallBackError(nErrorCode, errorText)


lngFile = "shortestPath.lng"

df = pd.read_csv("network.csv")

# Get the data from the dataframe
# into numpy arrays
ARCS = df.iloc[:,0:2].values
DIST = df.Distance.values
# The sourec is the start the sink is the finish
SOURCE = 1
SINK = 6
# there are six nodes in the network
NODECOUNT = 6
# X is the decision a binary descion variable for each arc in the network
X = np.zeros(len(ARCS))
# for checking if the model is optimal 
STATUS = np.array([-1.0])

# Create a model object
model = lingo.Model(lngFile , "log")
# set all pointers in the order that they appear in shortestPath.lng
model.set_pointer("Pointer1",NODECOUNT,lingo.PARAM)
model.set_pointer("Pointer2",ARCS,lingo.SET)
model.set_pointer("Pointer3",DIST,lingo.PARAM)
model.set_pointer("Pointer4",SOURCE,lingo.PARAM)
model.set_pointer("Pointer5",SINK,lingo.PARAM)
model.set_pointer("Pointer6",X,lingo.VAR)
model.set_pointer("Pointer7",STATUS,lingo.VAR)
# set the call back function and user data
model.set_cbError(cbError)
model.set_uData(uData)
# now that everything is set call solve(model)
lingo.solve(model)

# check that the model has ben solved
if STATUS[0] == lingo.LS_STATUS_GLOBAL_LNG:
    print("\nGlobal optimum found!")
elif STATUS[0] == lingo.LS_STATUS_LOCAL_LNG:
    print("\nLocal optimum found!")
else:
    print("\nSolution is non-optimal\n")

# output the objective value and path.
objVal = np.sum(DIST*X)
path = ARCS[X.astype(bool)]
print("Cost: ",objVal)
pathstr = f"Shortest Path: {path[0][0]} -> {path[0][1]} -> "
for i in range(1,len(path) - 1):
    pathstr += f"{path[i][1]} -> "
pathstr += f"{path[-1][1]}"
print(pathstr)