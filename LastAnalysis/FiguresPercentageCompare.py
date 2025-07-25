import numpy as np
import seaborn as sns
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from matplotlib import pyplot as plt

DepolBlock = False
Fit = False
ConditionAux = 'MirrorDecre'

colors = {'InVivo': 'C2', 'MirrorDecre': 'C1', 'OnlyIncre': 'C0'}

folderLoad = "spikes2S_500"
folderSave = "figuresPercentage2SCompare_500"

fitLinear = False

WindowSize = 250
MovementTime = 1800
TimeWindow1 = [MovementTime - WindowSize, MovementTime]
TimeWindow2 = [MovementTime, MovementTime + WindowSize]
TimeWindow3 = [MovementTime + WindowSize, MovementTime + 2 * WindowSize]

SecondMovementTime = 1800 + 500
TimeWindow4 = [SecondMovementTime - WindowSize, SecondMovementTime]
TimeWindow5 = [SecondMovementTime, SecondMovementTime + WindowSize]
TimeWindow6 = [SecondMovementTime + WindowSize, SecondMovementTime + 2 * WindowSize]

ThirdMovementTime = 1800 + 1000
TimeWindow7 = [ThirdMovementTime - WindowSize, ThirdMovementTime]
TimeWindow8 = [ThirdMovementTime, ThirdMovementTime + WindowSize]
TimeWindow9 = [ThirdMovementTime + WindowSize, ThirdMovementTime + 2 * WindowSize]

TimeWindows = [TimeWindow2, TimeWindow5, TimeWindow8]#[TimeWindow1, TimeWindow2, TimeWindow3, TimeWindow4, TimeWindow5, TimeWindow6, TimeWindow7, TimeWindow8, TimeWindow9]

for TimeWindow in TimeWindows:
    for factorAmpAux in [0.5, 1, 2]:
        for factorWidthAux in [1]:

            with open(folderLoad+"/DataDepol%sFit%sA_%sW%s.pkl" % (DepolBlock, Fit, factorAmpAux, factorWidthAux), 'rb') as f:
                dataDict = pickle.load(f)

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

            data = dataFrame[(dataFrame['Ntotal']==N)*(dataFrame['Condition']==ConditionAux)][['%PT5B_inc', 'FoxP2Rate', 'Condition', 'Impedance']]


            data[['%PT5B_inc', 'FoxP2Rate', 'Impedance']] = data[['%PT5B_inc', 'FoxP2Rate', 'Impedance']].astype(float)

            # sns.lineplot(x='%PT5B_inc', y='FoxP2Rate', hue='Condition', data=data)
            if fitLinear:
                from scipy import stats
                slope, intercept, r_value, p_value, std_err, quadratic = {}, {}, {}, {}, {}, {}

                for Condition in [ConditionAux]:
                    dataAux = data[(dataFrame['Condition']==Condition)][['%PT5B_inc', 'FoxP2Rate', 'Impedance']]
                    if Condition == 'OnlyIncre':
                        model = np.polyfit(dataAux['%PT5B_inc'].values,dataAux['FoxP2Rate'].values, 2)
                    else:
                        slope[Condition], intercept[Condition], r_value[Condition], p_value[Condition], std_err[Condition] = stats.linregress(dataAux['%PT5B_inc'].values,dataAux['FoxP2Rate'].values)

            variable = 'FoxP2Rate'

            fig = plt.figure(1)
            ax = fig.gca()

            if ConditionAux == 'OnlyIncre':
                order=2
            else:
                order=1
            if fitLinear:
                fgrid = sns.regplot(x='%PT5B_inc', y=variable, ax=ax, data=data, x_estimator=np.mean, color=colors[ConditionAux], order=order)
                for Condition in [ConditionAux]:
                    if Condition == 'OnlyIncre':
                        ax.annotate(
                            '%s quad= %2.2f ' % (Condition, model[0]) + ' slope= %2.2f ' % (model[1]),
                            (50, model[0]*40.**2+model[1]*40+model[2]))
                    else:
                        ax.annotate('%s slope= %2.2f ' % (Condition, slope[Condition]) + "p = {:.2E}".format( p_value[Condition]), (50,slope[Condition]*40+intercept[Condition]))
            else:
                sns.lineplot(x='%PT5B_inc', y=variable, data=data, color=colors[ConditionAux])
                # sns.pointplot(x='%PT5B_inc', y=variable, data=data, color=colors[ConditionAux])
            plt.ylim([0,160])

    plt.savefig(folderSave+"/%sDepol%sFit%sA_%sW%s_N%s_%s_%s.eps" % (variable, DepolBlock, Fit, factorAmpAux, factorWidthAux, N, TimeWindow, ConditionAux))
    plt.close()
    # plt.show()
