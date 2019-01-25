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
outputGraphName = sys.argv[2]+'.png'

runTimes = pd.read_csv(filenamePath, names=['Input_Size', 'Run_Times'])

runTimes = runTimes.sort_values(by=['Input_Size'])
runTimes = runTimes.drop_duplicates(subset=['Input_Size'], keep='first')

fig = runTimes.plot(x='Input_Size', y='Run_Times')
fig.legend([sys.argv[1].split('.')[0]])

# fig = runTimes.plot()


fig = fig.get_figure()


fig.savefig(sys.argv[2])

