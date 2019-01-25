# Siddharth Agarwal
# 1001577570
# 
# python finalPlotModule.py <input file name with extension> <output graph name without extension >
# for example
# python finalPlotModule.py runtime.txt testPlot2

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filenamePath = './'+sys.argv[1]

runTimes = pd.read_csv(filenamePath)

header = runTimes.columns.values.tolist()
outputGraphName = header[0]+'.png'
# runTimes = runTimes.sort_values(by=['Input_Size'])
# runTimes = runTimes.drop_duplicates(subset=['Input_Size'], keep='first')

fig = runTimes.plot()
fig.legend([header[0]])

# fig = runTimes.plot()


fig = fig.get_figure()


fig.savefig(header[0])

