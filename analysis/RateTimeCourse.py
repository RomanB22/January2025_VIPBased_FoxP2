import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import auxFuncs

depolBlock = True
if depolBlock:
    folder = 'figuresDepol'
else:
    folder = 'figuresNoDepol'
df = pd.read_pickle("results/NeuronalArithmeticDepol%s.pkl" % depolBlock)

# Figures to create FoxP2 rate vs PT5B rate Inc for several PT5B Dec rate.
# We need to choose a time window and condition

Condition = 'InVivo'
TimeWindow = [1200, 3600]
NoisePresent = str(True)
SynsPerConn = 1
AMPAWeight = 0.001

dfMasked = df[(df['Condition'] == Condition) &
              (df['Time'] >= TimeWindow[0]) & (df['Time'] <= TimeWindow[1])
              & (df['NoisePresent'] == NoisePresent)
              & (df['SynsPerConn'] == SynsPerConn)
              & (df['AMPAWeight'] == AMPAWeight)][['NumIncreasing', 'NumDecreasing', 'Time',
                                                   'FoxP2Rate', 'DecRate', 'IncRate']]

X_vector = []
Y_vector = []
Z_vector = []
Surface_vector = []
Variable = 'NumDecreasing' # 'NumIncreasing' 'NumDecreasing' 'Time'
NumDecreasing = np.unique(dfMasked[Variable])[3] # NumDecreasing [25 51 76 102 127 153 178 204 229 255]
                                           # NumIncreasing [9 18 27 36 45 54 63 72 81 90]
# Time windows [1250. 1350. 1450. 1550. 1650. 1750. 1850. 1950. 2050. 2150. 2250. 2350.
#  2450. 2550. 2650. 2750. 2850. 2950. 3050. 3150. 3250. 3350. 3450. 3550.]

dfMasked2 = dfMasked[df[Variable] == NumDecreasing]

# Re-index rows
dfMasked2.index = range(len(dfMasked2))

for i in range(len(dfMasked2)):
    Z_vector.append(dfMasked2['FoxP2Rate'][i])
    if Variable == 'NumDecreasing':
        X_vector.append(dfMasked2['Time'][i])
        Y_vector.append(dfMasked2['IncRate'][i])
        Surface_vector.append(dfMasked2['DecRate'][i])
        ylabel = 'PT5B Inc Rate (Hz)'
        xlabel = 'Time (ms)'
        zlabel = 'FoxP2 Rate (Hz)'
        trajlabels = '$r_{PT5B_{Inc}}$: $%1.2f$ $Hz$'
        legendlabel = '$r_{PT5B_{Dec}}$: $%1.2f$ $Hz$'
        TimeImplicit = False
        indexInVivo = 4 #3
        InVivoInputs = np.unique(df[Variable])[3]
    elif Variable == 'NumIncreasing':
        X_vector.append(dfMasked2['Time'][i])
        Y_vector.append(dfMasked2['DecRate'][i])
        Surface_vector.append(dfMasked2['IncRate'][i])
        ylabel = 'PT5B Dec Rate (Hz)'
        xlabel = 'Time (ms)'
        zlabel = 'FoxP2 Rate (Hz)'
        trajlabels = '$r_{PT5B_{Dec}}$: $%1.2f$ $Hz$'
        legendlabel = '$r_{PT5B_{Inc}}$: $%1.2f$ $Hz$'
        TimeImplicit = False
        indexInVivo = 3
        InVivoInputs = np.unique(df[Variable])[3]
    elif Variable == 'Time':
        X_vector.append(dfMasked2['IncRate'][i])
        Y_vector.append(dfMasked2['DecRate'][i])
        Surface_vector.append(dfMasked2['Time'][i])
        ylabel = 'PT5B Dec Rate (Hz)'
        xlabel = 'PT5B Inc Rate (Hz)'
        zlabel = 'FoxP2 Rate (Hz)'
        trajlabels = '$r_{PT5B_{Dec}}$: $%1.2f$ $Hz$'
        legendlabel = '$r_{Time}$: $%1.2f$ $ms$'
        TimeImplicit = True
        indexInVivo = 3
        InVivoInputs = 3

X_vector = np.array(X_vector).flatten()
Y_vector = np.array(Y_vector).flatten()
Z_vector = np.array(Z_vector).flatten()

auxFuncs.PlotSurface(X_vector, Y_vector, Z_vector, NumDecreasing, Surface_vector, InVivoInputs=InVivoInputs, indexInVivo=indexInVivo,
                     TimeImplicit=TimeImplicit,
                     xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, legendlabel=legendlabel, trajlabels=trajlabels)
plt.show()

if TimeImplicit:
    auxFuncs.PlotRate3D(X_vector, Y_vector, Z_vector, NumDecreasing, InVivoInputs=InVivoInputs, indexInVivo=indexInVivo,
                        marker='x', mode='xz',
                        colormap='viridis',
                        xlabel=xlabel, ylabel=zlabel, TimeImplicit=TimeImplicit, legendlabel=trajlabels)
    plt.show()

    auxFuncs.PlotRate3D(X_vector, Y_vector, Z_vector, NumDecreasing, InVivoInputs=InVivoInputs, marker='x', mode='yz',
                        colormap='viridis', xlabel=ylabel, ylabel=zlabel, TimeImplicit=TimeImplicit,
                        legendlabel=trajlabels)
    plt.show()
else:
    auxFuncs.PlotRate3D(X_vector, Y_vector, Z_vector, NumDecreasing, InVivoInputs=InVivoInputs, marker='x', mode='xz', colormap='viridis',
                        xlabel=xlabel, ylabel=zlabel, TimeImplicit=TimeImplicit, legendlabel=trajlabels)
    plt.show()

    auxFuncs.PlotRate3D(X_vector, Y_vector, Z_vector, NumDecreasing, InVivoInputs=InVivoInputs, marker='x', mode='xy', colormap='viridis',
                        xlabel=xlabel, ylabel=ylabel, TimeImplicit=TimeImplicit, legendlabel=trajlabels)
    plt.show()

    auxFuncs.PlotRate3D(X_vector, Y_vector, Z_vector, NumDecreasing, InVivoInputs=InVivoInputs, marker='x', mode='yz',
                        colormap='viridis', xlabel=ylabel, ylabel=zlabel, TimeImplicit=TimeImplicit, legendlabel=trajlabels)
    plt.show()