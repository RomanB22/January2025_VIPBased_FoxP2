import pickle

# from matplotlib import pyplot as plt

import auxFuncs as aux
import numpy as np
import pandas as pd
# import seaborn as sns

Fit = False
constantArea = False
folderLoad = 'resultsExpInputs'
folderSave = 'resultsExpInputs'

saveDataFrame = True

for factorAmpAux in [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]:
    for factorWidthAux in [1.0]:#[0.5,1.,2.]:
        with open(folderLoad + "/SimSpikesFit%sA_%sW%s_Area%s.pkl" % (Fit, factorAmpAux, factorWidthAux, constantArea), 'rb') as f:
            dataDict = pickle.load(f)

        columns = ['Condition', 'NumIncreasing', 'NumDecreasing', 'NumNotRelated', 'Ntotal', 'NoisePresent',
                   'AMPAWeight', 'SynsPerConn', 'IAmp', '%PT5B_inc', 'Time', 'FoxP2Rate', 'DecRate', 'IncRate',
                   'BgRate', 'Impedance', 'Trial']

        dt = 1  # ms
        window_size = 50  # in time will be window_size*dt
        MovementTime = 1800
        PreWindow_start = 0
        PreWindow_end = MovementTime
        PostWindow_start = MovementTime
        PostWindow_end = 3800

        df = pd.DataFrame(columns=columns)

        for key, value in dataDict.items():
            (Condition, NumIncreasing, NumDecreasing, NumNotRelated, NetStimPre, NetStimPost, NetStimNoise, AMPAWeight,
             SynsPerConn, IAmp, NoisePresent, factorAmp, factorWidth, Fitting) = key.split('_')

            NumIncreasing = int(NumIncreasing)
            NumDecreasing = int(NumDecreasing)
            NumNotRelated = int(NumNotRelated)
            SynsPerConn = int(SynsPerConn)
            NetStimPre = float(NetStimPre)
            NetStimPost = float(NetStimPost)
            NetStimNoise = float(NetStimNoise)
            AMPAWeight = float(AMPAWeight)
            IAmp = float(IAmp)
            factorAmp = float(factorAmp)
            factorWidth = float(factorWidth)
            Fitting = Fitting

            print(Condition, NumIncreasing, NumDecreasing, NumNotRelated, NetStimPre, NetStimPost, NetStimNoise, AMPAWeight,
                 SynsPerConn, IAmp, NoisePresent, factorAmp, factorWidth, Fitting)

            SpikesFoxP2 = value['SpikeFoxP2']
            SpikesDecre = value['SpikeDecre']
            SpikesIncre = value['SpikeIncre']
            SpikesBackground = value['SpikeBackground']
            ImpedanceValue = np.array(value['Impedance']['Value']).T
            ImpedanceRecTime = np.array(value['Impedance']['Time']) # unused

            time = np.arange(PreWindow_start, PostWindow_end, window_size * dt)

            if not len(ImpedanceRecTime)==len(time): raise ValueError('ImpedanceRecTime and time are not the same length')

            RateFoxP2, RateDec, RateInc, RateBackground = aux.CalculateRateNew(SpikesFoxP2, SpikesDecre, SpikesIncre,
                                                                               SpikesBackground, window_size, dt,
                                                                               PreWindow_start, PostWindow_end)



            # columns = ['Condition', 'NumIncreasing', 'NumDecreasing', 'NumNotRelated',  'Ntotal',
            #            'NoisePresent', 'AMPAWeight', 'SynsPerConn', 'IAmp',
            #            '%PT5B_inc', 'Time', 'FoxP2Rate', 'DecRate', 'IncRate', 'BgRate', 'Impedance']

            auxColumn = [Condition, NumIncreasing, NumDecreasing, NumNotRelated, NumIncreasing+NumDecreasing+NumNotRelated,
                         NoisePresent, AMPAWeight, SynsPerConn, IAmp,
                         NumIncreasing*100./(NumIncreasing+NumDecreasing+NumNotRelated), time, RateFoxP2, RateDec, RateInc,
                         RateBackground, ImpedanceValue]

            for j in range(len(auxColumn[11])):
                dict = [{'Condition': auxColumn[0],
                             'NumIncreasing': auxColumn[1],
                             'NumDecreasing': auxColumn[2],
                             'NumNotRelated': auxColumn[3],
                             'Ntotal': auxColumn[4],
                             'NoisePresent': auxColumn[5],
                             'AMPAWeight': auxColumn[6],
                             'SynsPerConn': auxColumn[7],
                             'IAmp': auxColumn[8],
                             '%PT5B_inc': auxColumn[9],
                             'Time': auxColumn[10],
                             'FoxP2Rate': auxColumn[11][j],
                             'DecRate': auxColumn[12][j],
                             'IncRate': auxColumn[13][j],
                             'BgRate': auxColumn[14][j],
                             'Impedance': auxColumn[15][j],
                             'Trial': j}]
                row = pd.DataFrame(dict, columns=columns)
                df = pd.concat([df, row], ignore_index=True)

        if saveDataFrame:
            df.to_pickle(folderSave+"/DataFit%sA_%sW%s_Area%s.pkl" % (Fit, factorAmpAux, factorWidthAux, constantArea))