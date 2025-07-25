import numpy as np
import seaborn as sns
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from matplotlib import pyplot as plt

DepolBlock = False
Fit = False
factorAmpAux=2
factorWidthAux=1

folderLoad = "spikes2S"
folderSave = "figuresPercentage2S"

with open(folderLoad+"/DataDepol%sFit%sA_%sW%s.pkl" % (DepolBlock, Fit, factorAmpAux, factorWidthAux), 'rb') as f:
    dataDict = pickle.load(f)

WindowSize = 250
MovementTime = 1800
TimeWindow1 = [MovementTime-WindowSize, MovementTime]
TimeWindow2 = [MovementTime, MovementTime+WindowSize]
TimeWindow3 = [MovementTime+WindowSize, MovementTime+2*WindowSize]

SecondMovementTime = 1800+1000
TimeWindow4 = [SecondMovementTime-WindowSize, SecondMovementTime]
TimeWindow5 = [SecondMovementTime, SecondMovementTime+WindowSize]
TimeWindow6 = [SecondMovementTime+WindowSize, SecondMovementTime+2*WindowSize]

TimeWindow = TimeWindow6
index = (dataDict['Time'].iloc[0]>=TimeWindow[0]) & (dataDict['Time'].iloc[0]<TimeWindow[1])

dataFrame = dataDict
for i in range(dataFrame.shape[0]):
    dataFrame['Time'].iloc[i] = np.mean(dataFrame['Time'].iloc[i][index], dtype=float)
    dataFrame['FoxP2Rate'].iloc[i] = np.mean(dataFrame['FoxP2Rate'].iloc[i][index], dtype=float)
    dataFrame['DecRate'].iloc[i] = np.mean(dataFrame['DecRate'].iloc[i][index], dtype=float)
    dataFrame['IncRate'].iloc[i] = np.mean(dataFrame['IncRate'].iloc[i][index], dtype=float)
    dataFrame['BgRate'].iloc[i] = np.mean(dataFrame['BgRate'].iloc[i][index], dtype=float)
    dataFrame['Impedance'].iloc[i] = np.mean(dataFrame['Impedance'].iloc[i][index], dtype=float)

# dataFrame = dataDict[['Condition','Ntotal','%PT5B_inc','FoxP2Rate','DecRate','IncRate','BgRate','Impedance','Trial']]
dataFrame = dataFrame[['Condition','Ntotal','%PT5B_inc','FoxP2Rate','DecRate','IncRate','BgRate','Impedance',
                       'NumIncreasing','NumDecreasing']]

N=8. # 2, 3, 8, 14, 20

data = dataFrame[(dataFrame['Ntotal']==N)][['%PT5B_inc', 'FoxP2Rate', 'Condition', 'Impedance']]


data[['%PT5B_inc', 'FoxP2Rate', 'Impedance']] = data[['%PT5B_inc', 'FoxP2Rate', 'Impedance']].astype(float)

# sns.lineplot(x='%PT5B_inc', y='FoxP2Rate', hue='Condition', data=data)
from scipy import stats
slope, intercept, r_value, p_value, std_err = {}, {}, {}, {}, {}
for Condition in data.Condition.unique():
    dataAux = data[(dataFrame['Condition']==Condition)][['%PT5B_inc', 'FoxP2Rate', 'Impedance']]
    slope[Condition], intercept[Condition], r_value[Condition], p_value[Condition], std_err[Condition] = stats.linregress(dataAux['%PT5B_inc'].values,dataAux['FoxP2Rate'].values)

variable = 'FoxP2Rate'

fgrid = sns.lmplot(x='%PT5B_inc', y=variable, hue='Condition', data=data, x_estimator=np.mean)
for ax in fgrid.axes[0]:
    for Condition in data.Condition.unique():
        ax.annotate('%s slope= %2.2f ' % (Condition, slope[Condition]) + "p = {:.2E}".format( p_value[Condition]), (50,slope[Condition]*40+intercept[Condition]))
plt.ylim([0,140])
plt.savefig(folderSave+"/%sDepol%sFit%sA_%sW%s_N%s_%s.eps" % (variable, DepolBlock, Fit, factorAmpAux, factorWidthAux, N, TimeWindow))
plt.close()
# plt.show()


