import xarray as xr
import pickle
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

depolBlock = False
with open("results/DataDepol%s.pkl" % depolBlock, 'rb') as f:
    dataDict = pickle.load(f)

dimensions = ["time", "pt5b_inc", "trial", "condition", "ntotal"]

timeCoord = [i-1800 for i in dataDict["Time"].iloc[0]]
pt5b_incCoord = np.unique(dataDict["%PT5B_inc"])
trialCoord = np.unique(dataDict["Trial"])
conditionCoord = np.unique(dataDict["Condition"])
nTotalCoord = np.unique(dataDict["Ntotal"])

Data = np.nan*np.zeros((5, len(timeCoord), len(pt5b_incCoord), len(trialCoord), len(conditionCoord), len(nTotalCoord)))

for i in range(dataDict.shape[0]):
    indexPT5B_inc = np.argwhere(pt5b_incCoord == dataDict["%PT5B_inc"][i])[0][0]
    indexTrial = np.argwhere(trialCoord == dataDict["Trial"][i])[0][0]
    indexCondition = np.argwhere(conditionCoord == dataDict["Condition"][i])[0][0]
    indexNtotal = np.argwhere(nTotalCoord == dataDict["Ntotal"][i])[0][0]


    Data[0,:,indexPT5B_inc, indexTrial, indexCondition, indexNtotal] = dataDict["DecRate"][i]
    Data[1,:,indexPT5B_inc, indexTrial, indexCondition, indexNtotal] = dataDict["IncRate"][i]
    Data[2,:,indexPT5B_inc, indexTrial, indexCondition, indexNtotal] = dataDict["BgRate"][i]
    Data[3,:,indexPT5B_inc, indexTrial, indexCondition, indexNtotal] = dataDict["FoxP2Rate"][i]
    Data[4,:,indexPT5B_inc, indexTrial, indexCondition, indexNtotal] = dataDict["Impedance"][i]

ds = xr.Dataset(
    data_vars={
        "DecRate": (dimensions, Data[0,:,:,:,:,:]),
        "IncRate": (dimensions, Data[1,:,:,:,:,:]),
        "BgRate": (dimensions, Data[2,:,:,:,:,:]),
        "FoxP2Rate": (dimensions, Data[3,:,:,:,:,:]),
        "Impedance": (dimensions, Data[4,:,:,:,:,:]),
    },
    coords={
        "time": timeCoord,
        "pt5b_inc": pt5b_incCoord,
        "trial": trialCoord,
        "condition": conditionCoord,
        "ntotal": nTotalCoord,
    },
)

Ntotal = 20
PT5BInc = 25
Condition = 'InVivo'
Time2Plot = (-1000,2000)

Ndec=Ntotal-int(Ntotal*PT5BInc/100.)
Ninc=int(Ntotal*PT5BInc/100.)

# print(ds.coords['pt5b_inc'].values, '\n', ds.coords['ntotal'].values)

plt.figure(1)
data2plot = ds.sel(ntotal=Ntotal, pt5b_inc=PT5BInc, time=slice(*Time2Plot)).coarsen(time=5, boundary='pad').mean().to_dataframe()
sns.lineplot(x='time', y='FoxP2Rate', hue='condition', data=data2plot)
plt.vlines(x=0, ymin=10, ymax=120, colors='k', linestyles='-', label='Movement')
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.legend(frameon=False)
# plt.savefig("FoxP2Time_%d.eps" % PT5BInc)
# plt.show()
plt.close()

plt.figure(2)
sns.lineplot(x='time', y='Impedance', hue='condition', data=data2plot)
plt.vlines(x=0, ymin=10, ymax=150, colors='k', linestyles='-', label='Movement')
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.legend(frameon=False)
# plt.savefig("Impedance_%d.eps" % PT5BInc)
# plt.show()
plt.close()

plt.figure(3)
data2plot_2 = ds.sel(ntotal=Ntotal, pt5b_inc=PT5BInc, condition=Condition, time=slice(*Time2Plot)).coarsen(time=5,boundary="trim").mean().to_dataframe()
data2plot_2['DecRate'] = data2plot_2['DecRate']/Ndec
data2plot_2['IncRate'] = data2plot_2['IncRate']/Ninc
# sns.lineplot(x='time', y='DecRate', data=data2plot_2, label='$PT5B_{dec}$')
# sns.lineplot(x='time', y='IncRate', data=data2plot_2, label='$PT5B_{inc}$')
sns.lineplot(x='time', y='BgRate', data=data2plot_2, label='$PT5B_{bg}$')
# plt.vlines(x=0, ymin=0, ymax=100, colors='k', linestyles='-', label='Movement')
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.legend(frameon=False)
# plt.savefig("2_InputsPerCell%s_%d.eps" % (Condition, PT5BInc))
# plt.show()
plt.close()


time1 = (-250,0)
time2 = (0,250)
time3 = (250,500)
baseline = (-1250,-1000)
Time2Plot = time3

peaksDict = {}

baselineDistanceDict = {}

from scipy.signal import find_peaks
for Condition in conditionCoord:
    peaksDict[str(Condition)]={}
    baselineDistanceDict[str(Condition)]={}
    for Ntotal in nTotalCoord:
        peaksDict[str(Condition)][str(Ntotal)]={}
        baselineDistanceDict[str(Condition)][str(Ntotal)]={}
        for PT5BInc in pt5b_incCoord:
            data2plotAux = ds.sel(ntotal=Ntotal, pt5b_inc=PT5BInc, condition=Condition).mean(dim='trial').to_dataframe()
            data2Baseline = ds.sel(ntotal=Ntotal, pt5b_inc=PT5BInc, condition=Condition, time=slice(*baseline)).mean(dim='trial').to_dataframe()

            data2plotAux['FoxP2Rate'] = data2plotAux['FoxP2Rate']-np.mean(data2Baseline['FoxP2Rate'])

            dataPeaks = data2plotAux['FoxP2Rate'].values

            baselineDistanceDict[str(Condition)][str(Ntotal)][str(PT5BInc)] = dataPeaks[-1]/np.mean(data2Baseline['FoxP2Rate'])

            peaks, properties = find_peaks(dataPeaks, prominence=10, width=20, height=0)

            if len(peaks)==0:
                continue

            x = data2plotAux['FoxP2Rate'].values

            zero_crossings = np.where(np.diff(np.sign(x)))[0]

            peak_widthLeft = zero_crossings[[i<peaks[0] for i in zero_crossings]][-1]
            try:
                peak_widthRight = zero_crossings[[i>peaks[0] for i in zero_crossings]][0]+1
            except:
                continue

            timepeaks = [timeCoord[i] for i in peaks]

            if timepeaks[0] <= 0:
                continue

            peakwidth = timeCoord[peak_widthRight]-timeCoord[peak_widthLeft]

            peaksDict[str(Condition)][str(Ntotal)][str(PT5BInc)] = peakwidth

            # if Ntotal==20:
            #     plt.figure(5)
            #     sns.lineplot(x='time', y='FoxP2Rate', data=data2plotAux)
            #     plt.plot(timepeaks, x[peaks], "x")
            #     plt.vlines(x=timepeaks, ymin=x[peaks] - properties["prominences"],
            #                ymax = x[peaks], color = "C1")
            #     plt.hlines(y=0, xmin=timeCoord[peak_widthLeft],
            #                xmax=timeCoord[peak_widthRight], color = "C1")
            #     plt.legend(frameon=False)
            #     ax = plt.gca()
            #     ax.spines['top'].set_visible(False)
            #     ax.spines['right'].set_visible(False)
            #     # ax.set_ylim(0, 130)
            #     # plt.savefig("FoxP2percentage_%d_%s.eps" % (PT5BInc, Time2Plot))
            #     plt.show()
            #     plt.close()

import pandas as pd
df = pd.DataFrame.from_dict(peaksDict)
dfDistance = pd.DataFrame.from_dict(baselineDistanceDict)

print(df)

color = {'2': 'C0','3': 'C1','8': 'C2','14': 'C4','20': 'C5'}

for i in df['InVivo'].index:
    percentagePT5B = []
    returnTime = []
    for key, value in df['InVivo'][i].items():
        percentagePT5B.append(float(key))
        returnTime.append(float(value))
    percentagePT5B = np.array(percentagePT5B).flatten()
    returnTime = np.array(returnTime).flatten()
    plt.plot(percentagePT5B, returnTime, marker='o', color=color[i], linewidth=0, label="In Vivo - N="+str(i))
plt.legend(frameon=False)
plt.xlabel("%PT5B_inc")
plt.xlim(0,100)
plt.ylabel("Return to baseline time (ms)")
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# plt.savefig("ReturnToBaseline.eps")
plt.show()

color = {'2': 'C0','3': 'C1','8': 'C2','14': 'C4','20': 'C5'}
indexAux=[2]#[1,2,3]

for i in dfDistance['InVivo'].index[indexAux]:
    percentagePT5B = []
    returnTime = []
    for key, value in dfDistance['InVivo'][i].items():
        percentagePT5B.append(float(key))
        returnTime.append(float(value))
    percentagePT5B = np.array(percentagePT5B).flatten()
    returnTime = np.array(returnTime).flatten()
    plt.plot(percentagePT5B, returnTime, marker='o', color=color[i], linewidth=0, label="In Vivo - N="+str(i))

for i in dfDistance['MirrorDecre'].index[indexAux]:
    percentagePT5B = []
    returnTime = []
    for key, value in dfDistance['MirrorDecre'][i].items():
        percentagePT5B.append(float(key))
        returnTime.append(float(value))
    percentagePT5B = np.array(percentagePT5B).flatten()
    returnTime = np.array(returnTime).flatten()
    plt.plot(percentagePT5B, returnTime, marker='x', color=color[i], linewidth=0, label="Not decreasing PT_dec - N="+str(i))

for i in dfDistance['OnlyIncre'].index[indexAux]:
    percentagePT5B = []
    returnTime = []
    for key, value in dfDistance['OnlyIncre'][i].items():
        percentagePT5B.append(float(key))
        returnTime.append(float(value))
    percentagePT5B = np.array(percentagePT5B).flatten()
    returnTime = np.array(returnTime).flatten()
    plt.plot(percentagePT5B, returnTime, marker='s', color=color[i], linewidth=0, label="Only PT_inc- N="+str(i))
plt.legend(frameon=False)
plt.hlines(linestyles='--', color='k', y=0, xmin=0, xmax=100)
plt.xlabel("%PT5B_inc")
plt.xlim(-5,105)
plt.ylabel("Distance to baseline rate (Hz)")
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# plt.savefig("DistanceToBaseline.eps")
plt.show()

