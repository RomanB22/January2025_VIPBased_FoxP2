import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import auxFuncs

depolBlock = False
if depolBlock:
    folder = 'figuresDepol'
else:
    folder = 'figuresNoDepol'
df = pd.read_pickle("results/NeuronalArithmeticDepol%s.pkl" % depolBlock)

# Figures to create FoxP2 rate vs PT5B rate Inc for several PT5B Dec rate.
# We need to choose a time window and condition

Condition = 'InVivo'
TimeWindow = [800, 3600]
NoisePresent = str(True)
SynsPerConn = 1
AMPAWeight = 0.002

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
Index = 1 #1
NumDecreasing = np.unique(dfMasked[Variable])[Index] # NumDecreasing [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41]
                                           # NumIncreasing [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41]
# Time windows [ 825.  875.  925.  975. 1025. 1075. 1125. 1175. 1225. 1275. 1325. 1375.
#  1425. 1475. 1525. 1575. 1625. 1675. 1725. 1775. 1825. 1875. 1925. 1975.
#  2025. 2075. 2125. 2175. 2225. 2275. 2325. 2375. 2425. 2475. 2525. 2575.
#  2625. 2675. 2725. 2775. 2825. 2875. 2925. 2975. 3025. 3075. 3125. 3175.
#  3225. 3275. 3325. 3375. 3425. 3475. 3525. 3575.]

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
        indexInVivo = 1
        InVivoInputs = np.unique(df[Variable])[1]
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
        indexInVivo = 1
        InVivoInputs = np.unique(df[Variable])[1]
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
        indexInVivo = 1
        InVivoInputs = 1

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