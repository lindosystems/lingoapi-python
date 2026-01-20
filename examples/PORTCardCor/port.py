


import lingo_api as lingo
import numpy as np
#import pandas as pd

#assetsDF = pd.read_csv("assets.csv")

lngFile = "PORTCardCor.lng"

CARD = 4
TARGET = 1.07


model = lingo.Model(lngFile)
lingo.solve(model)