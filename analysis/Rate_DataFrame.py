import numpy as np
import matplotlib.pyplot as plt
import pickle
import auxFuncs
import pandas as pd

DepolBlock=True
with open("results/SimSpikesDepol%s.pkl" % DepolBlock, 'rb') as f:
    dataDict = pickle.load(f)

# Each entry in the dictionary has the following info: Condition, NumIncreasing, NumDecreasing, NumNotRelated,
# NetStimPre, NetStimPost, NetStimNoise, AMPAWeight, SynsPerConn, IAmp, NoisePresent
# Inside eahc entry, it has the following keys: ['SpikeFoxP2', 'SpikeDecre', 'SpikeIncre']
# In the inputs, this is just aggregate spikes for every trial and each subpopulation. In order to calculate per
# neuron average firing rate for the inputs I have to calculate the average firing rate and divide it by the
# number of cells
InVivoPerCellAvg_DecrePre, InVivoPerCellAvg_IncrePre, InVivoPerCellAvg_DecrePost, InVivoPerCellAvg_IncrePost = 1.5, 0.8, 0.7, 3.4
MirrorDecrePerCellAvg_DecrePre, MirrorDecrePerCellAvg_IncrePre, MirrorDecrePerCellAvg_DecrePost, MirrorDecrePerCellAvg_IncrePost = 1.5, 0.8, 1.5, 3.4
OnlyIncrePerCellAvg_DecrePre, OnlyIncrePerCellAvg_IncrePre, OnlyIncrePerCellAvg_DecrePost, OnlyIncrePerCellAvg_IncrePost = 0, 0.8, 0, 3.4

columns = ['Condition', 'NumIncreasing', 'NumDecreasing', 'NumNotRelated',
           'NetStimPre', 'NetStimPost', 'NetStimNoise', 'NoisePresent',
           'AMPAWeight', 'SynsPerConn', 'IAmp',
           'Time', 'FoxP2Rate', 'DecRate', 'IncRate']
df = pd.DataFrame(columns=columns)

for k, v in dataDict.items():
    (Condition, NumIncreasing, NumDecreasing, NumNotRelated, NetStimPre,
     NetStimPost, NetStimNoise, AMPAWeight, SynsPerConn, IAmp, NoisePresent) = k.split('_')
    NumIncreasing = int(NumIncreasing)
    NumDecreasing = int(NumDecreasing)
    NumNotRelated = int(NumNotRelated)
    SynsPerConn = int(SynsPerConn)
    NetStimPre = float(NetStimPre)
    NetStimPost = float(NetStimPost)
    NetStimNoise = float(NetStimNoise)
    AMPAWeight = float(AMPAWeight)
    IAmp = float(IAmp)

    dt = 1  # ms
    window_size = 100  # in time will be window_size*dt
    MovementTime = 1800
    PreWindow_start = 0
    PreWindow_end = MovementTime
    PostWindow_start = MovementTime
    PostWindow_end = 3600
    time = np.arange(PreWindow_start + window_size / 2, PostWindow_end + window_size / 2, window_size * dt)

    SpikesFoxP2 = v['SpikeFoxP2']
    SpikesDec = v['SpikeDecre']
    SpikesInc = v['SpikeIncre']

    # Calculate rate for each trial and population
    RateFoxP2, RateDec, RateInc = auxFuncs.CalculateRate(SpikesFoxP2, SpikesDec, SpikesInc, window_size, dt,
                                                         PreWindow_start, PostWindow_end)

    # Calculate average rate and standard deviation
    FoxP2_avg, Dec_avg, Inc_avg, FoxP2_std, Dec_std, Inc_std = auxFuncs.CalculateAvgStd(RateFoxP2, RateDec, RateInc)
    # auxFuncs.PlotRate(FoxP2_avg, Dec_avg, Inc_avg, FoxP2_std, Dec_std, Inc_std, time)
    # plt.show()

    for i in range(len(time)):
        dict = [{'Condition': Condition,
                'NumIncreasing': NumIncreasing,
                'NumDecreasing': NumDecreasing,
                'NumNotRelated': NumNotRelated,
                'NetStimPre': NetStimPre,
                'NetStimPost': NetStimPost,
                'NetStimNoise': NetStimNoise,
                'NoisePresent': NoisePresent,
                'AMPAWeight': AMPAWeight,
                'SynsPerConn': SynsPerConn,
                'IAmp': IAmp,
                'Time': time[i],
                'FoxP2Rate': FoxP2_avg[i],
                'DecRate': Dec_avg[i],
                'IncRate': Inc_avg[i]}]
        row = pd.DataFrame(dict, columns=columns)
        df = pd.concat([df, row], ignore_index=True)

df.to_pickle("results/NeuronalArithmeticDepol%s.pkl" % DepolBlock)