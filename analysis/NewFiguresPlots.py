import numpy as np
import seaborn as sns
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from matplotlib import pyplot as plt

depolBlock = False
with open("results/DataDepol%s.pkl" % depolBlock, 'rb') as f:
    dataDict = pickle.load(f)

WindowSize = 250
MovementTime = 1800
TimeWindow1 = [MovementTime-WindowSize, MovementTime]
TimeWindow2 = [MovementTime, MovementTime+WindowSize]
TimeWindow3 = [MovementTime+WindowSize, MovementTime+2*WindowSize]

TimeWindow = TimeWindow1
index = (dataDict['Time'].iloc[0]>=TimeWindow1[0]) & (dataDict['Time'].iloc[0]<TimeWindow1[1])


dataFrame = dataDict
for i in range(dataFrame.shape[0]):
    dataFrame['Time'].iloc[i] = np.mean(dataFrame['Time'].iloc[i][index])
    dataFrame['FoxP2Rate'].iloc[i] = np.mean(dataFrame['FoxP2Rate'].iloc[i][index])
    dataFrame['DecRate'].iloc[i] = np.mean(dataFrame['DecRate'].iloc[i][index])
    dataFrame['IncRate'].iloc[i] = np.mean(dataFrame['IncRate'].iloc[i][index])
    dataFrame['BgRate'].iloc[i] = np.mean(dataFrame['BgRate'].iloc[i][index])
    dataFrame['Impedance'].iloc[i] = np.mean(dataFrame['Impedance'].iloc[i][index])

# dataFrame = dataDict[['Condition','Ntotal','%PT5B_inc','FoxP2Rate','DecRate','IncRate','BgRate','Impedance','Trial']]
dataFrame = dataFrame[['Condition','Ntotal','%PT5B_inc','FoxP2Rate','DecRate','IncRate','BgRate','Impedance']]

N=8

sns.lineplot(x='%PT5B_inc', y='Impedance', hue='Condition', style='Ntotal', data=dataFrame[dataFrame['Ntotal']==N])
plt.show()


