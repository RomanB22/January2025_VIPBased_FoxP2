import numpy as np
import matplotlib.pyplot as plt
import pickle
import auxFuncs

depolBlock = True
if depolBlock:
    folder = 'figuresDepol'
else:
    folder = 'figuresNoDepol'

with open("results/SimSpikesDepol%s.pkl" % depolBlock, 'rb') as f:
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
    window_size = 100 # in time will be window_size*dt
    PreWindow_start = 1200
    PreWindow_end = 1800
    PostWindow_start = 1800
    PostWindow_end = 3600
    time = np.arange(PreWindow_start+window_size/2, PostWindow_end+window_size/2, window_size*dt)

    SpikesFoxP2 = v['SpikeFoxP2']
    SpikesDec = v['SpikeDecre']
    SpikesInc = v['SpikeIncre']

    # Calculate rate for each trial and population
    RateFoxP2, RateDec, RateInc = auxFuncs.CalculateRate(SpikesFoxP2, SpikesDec, SpikesInc, window_size, dt, PreWindow_start, PostWindow_end)
    # print(k)
    # auxFuncs.PlotRaster(RateFoxP2, RateDec, RateInc, time)
    # plt.show()

    # Calculate average rate and standard deviation
    FoxP2_avg, Dec_avg, Inc_avg, FoxP2_std, Dec_std, Inc_std = auxFuncs.CalculateAvgStd(RateFoxP2, RateDec, RateInc)
    auxFuncs.PlotRate(FoxP2_avg, Dec_avg, Inc_avg, FoxP2_std, Dec_std, Inc_std, time)
    plt.title(k)
    plt.savefig(folder+'/Rate_%s.png' % k)
    plt.close()

    # Z-normalized rate
    FoxP2Raster_znorm, DecRaster_znorm, IncRaster_znorm = auxFuncs.CalculateZNorm(RateFoxP2, RateDec, RateInc)
    FoxP2_Zavg, Dec_Zavg, Inc_Zavg, FoxP2_Zstd, Dec_Zstd, Inc_Zstd = auxFuncs.CalculateAvgStd(FoxP2Raster_znorm, DecRaster_znorm, IncRaster_znorm)
    auxFuncs.PlotRate(FoxP2_Zavg, Dec_Zavg, Inc_Zavg, FoxP2_Zstd, Dec_Zstd, Inc_Zstd, time, Znormed=True)
    plt.title(k)
    plt.savefig(folder+'/Z_Rate_%s.png' % k)
    plt.close()

    # Difference between input and output rate
    FoxP2_IncRate_diff, FoxP2_DecRate_diff, Inc_DecRaster_diff = auxFuncs.CalculateDifference(RateFoxP2, RateDec, RateInc)
    # Avg and std
    FoxP2Inc_avg, FoxP2Dec_avg, IncDec_avg, FoxP2Inc_std, FoxP2Dec_std, IncDec_std = auxFuncs.CalculateAvgStd(FoxP2_IncRate_diff, FoxP2_DecRate_diff, Inc_DecRaster_diff)

    auxFuncs.PlotDiff(FoxP2Inc_avg, FoxP2Dec_avg, IncDec_avg, FoxP2Inc_std, FoxP2Dec_std, IncDec_std, time,
                      label=['FoxP2 - Inc', 'FoxP2 - Dec', 'Inc - Dec'])
    plt.title(k)
    plt.savefig(folder+'/Diff_%s.png' % k)
    plt.close()
    # Difference between z-normed rates
    FoxP2_IncRate_diff, FoxP2_DecRate_diff, Inc_DecRaster_diff = auxFuncs.CalculateDifference(FoxP2Raster_znorm, DecRaster_znorm, IncRaster_znorm)
    # auxFuncs.PlotRaster(FoxP2_IncRate_diff, FoxP2_DecRate_diff, Inc_DecRaster_diff, time)
    # plt.show()
    # Avg and std
    FoxP2Inc_avg, FoxP2Dec_avg, IncDec_avg, FoxP2Inc_std, FoxP2Dec_std, IncDec_std = auxFuncs.CalculateAvgStd(FoxP2_IncRate_diff, FoxP2_DecRate_diff, Inc_DecRaster_diff)

    auxFuncs.PlotDiff(FoxP2Inc_avg, FoxP2Dec_avg, IncDec_avg, FoxP2Inc_std, FoxP2Dec_std, IncDec_std, time,
                      label=['FoxP2 - Inc', 'FoxP2 - Dec', 'Inc - Dec'])
    plt.title(k)
    plt.savefig(folder+'/Z_Diff_%s.png' % k)
    plt.close()


