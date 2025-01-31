import numpy as np
import matplotlib.pyplot as plt
import pickle
import auxFuncs
from scipy.stats import pearsonr

depolBlock = False
if depolBlock:
    folder = 'figuresDepol'
else:
    folder = 'figuresNoDepol'

with open("results/SimSpikesDepol%s.pkl" % depolBlock, 'rb') as f:
    dataDict = pickle.load(f)

MatrixInVivo = []
MatrixMirrorDecre = []
MatrixOnlyIncre = []

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

    if AMPAWeight!=0.002: continue

    dt = 1  # ms
    window_size = 50 # in time will be window_size*dt
    Window1_start = 1800-250
    Window1_end = 1800+500
    Window2_start = 1800+500
    Window2_end = 1800+1250

    SpikesFoxP2 = v['SpikeFoxP2']
    SpikesDec = v['SpikeDecre']
    SpikesInc = v['SpikeIncre']

    # Calculate rate for each trial and population
    RateFoxP2_w1, RateDec_w1, RateInc_w1 = auxFuncs.CalculateRate(SpikesFoxP2, SpikesDec, SpikesInc, window_size, dt, Window1_start, Window1_end)
    RateFoxP2_w2, RateDec_w2, RateInc_w2 = auxFuncs.CalculateRate(SpikesFoxP2, SpikesDec, SpikesInc, window_size, dt, Window2_start, Window2_end)

    # RateFoxP2_w1, RateDec_w1, RateInc_w1 = auxFuncs.CalculateZNorm(RateFoxP2_w1, RateDec_w1, RateInc_w1)
    # RateFoxP2_w2, RateDec_w2, RateInc_w2 = auxFuncs.CalculateZNorm(RateFoxP2_w2, RateDec_w2, RateInc_w2)

    # RateFoxP2_w1, RateDec_w1, RateInc_w1 = RateFoxP2_w1.mean(axis=0), RateDec_w1.mean(axis=0), RateInc_w1.mean(axis=0)
    # RateFoxP2_w2, RateDec_w2, RateInc_w2 = RateFoxP2_w2.mean(axis=0), RateDec_w2.mean(axis=0), RateInc_w2.mean(axis=0)

    # Calculate correlations between input and output for each trial
    CorrFoxP2Inc_w1 = pearsonr(RateFoxP2_w1, RateInc_w1, axis=1).statistic
    CorrFoxP2Dec_w1 = pearsonr(RateFoxP2_w1, RateDec_w1, axis=1).statistic
    CorrFoxP2Inc_w2 = pearsonr(RateFoxP2_w2, RateInc_w2, axis=1).statistic
    CorrFoxP2Dec_w2 = pearsonr(RateFoxP2_w2, RateDec_w2, axis=1).statistic

    CorrFoxP2Inc_w1 = np.nanmean(CorrFoxP2Inc_w1)
    CorrFoxP2Dec_w1 = np.nanmean(CorrFoxP2Dec_w1)
    CorrFoxP2Inc_w2 = np.nanmean(CorrFoxP2Inc_w2)
    CorrFoxP2Dec_w2 = np.nanmean(CorrFoxP2Dec_w2)

    if str(Condition) == 'InVivo':
        MatrixInVivo.append([RateInc_w1.mean()/NumIncreasing, RateDec_w1.mean()/NumDecreasing, CorrFoxP2Inc_w1, CorrFoxP2Dec_w1, RateInc_w2.mean()/NumIncreasing, RateDec_w2.mean()/NumDecreasing, CorrFoxP2Inc_w2, CorrFoxP2Dec_w2])
    elif str(Condition) == 'MirrorDecre':
        MatrixMirrorDecre.append([RateInc_w1.mean()/NumIncreasing, RateDec_w1.mean()/NumDecreasing, CorrFoxP2Inc_w1, CorrFoxP2Dec_w1, RateInc_w2.mean()/NumIncreasing, RateDec_w2.mean()/NumDecreasing, CorrFoxP2Inc_w2, CorrFoxP2Dec_w2])
    elif str(Condition) == 'OnlyIncre':
        MatrixOnlyIncre.append([RateInc_w1.mean()/NumIncreasing, RateDec_w1.mean()/NumDecreasing, CorrFoxP2Inc_w1, CorrFoxP2Dec_w1, RateInc_w2.mean()/NumIncreasing, RateDec_w2.mean()/NumDecreasing, CorrFoxP2Inc_w2, CorrFoxP2Dec_w2])

    # plt.title('%s_%s' % (NumIncreasing, NumDecreasing))
    # plt.plot(RateFoxP2_w1, label='FoxP2')
    # plt.plot(RateDec_w1, label='Decreased')
    # plt.plot(RateInc_w1, label='Increased')
    # plt.legend(loc='best')
    # plt.show()
    # print(RateFoxP2_w1, RateDec_w1, RateInc_w1); quit()

MatrixInVivo = np.array(MatrixInVivo)
MatrixMirrorDecre = np.array(MatrixMirrorDecre)
MatrixOnlyIncre = np.array(MatrixOnlyIncre)

# RateInc_w1.mean()/NumIncreasing, RateDec_w1.mean()/NumDecreasing, CorrFoxP2Inc_w1, CorrFoxP2Dec_w1, RateInc_w2.mean()/NumIncreasing, RateDec_w2.mean()/NumDecreasing, CorrFoxP2Inc_w2, CorrFoxP2Dec_w2

AvgIncreInVivo_w1 = np.nanmean(MatrixInVivo[:,0])
AvgDecreInVivo_w1 = np.nanmean(MatrixInVivo[:,1])
AvgIncreInVivo_w2 = np.nanmean(MatrixInVivo[:,4])
AvgDecreInVivo_w2 = np.nanmean(MatrixInVivo[:,5])

AvgIncreMirrorDecre_w1 = np.nanmean(MatrixMirrorDecre[:,0])
AvgDecreMirrorDecre_w1 = np.nanmean(MatrixMirrorDecre[:,1])
AvgIncreMirrorDecre_w2 = np.nanmean(MatrixMirrorDecre[:,4])
AvgDecreMirrorDecre_w2 = np.nanmean(MatrixMirrorDecre[:,5])

AvgIncreOnlyIncre_w1 = np.nanmean(MatrixOnlyIncre[:,0])
AvgDecreOnlyIncre_w1 = np.nanmean(MatrixOnlyIncre[:,1])
AvgIncreOnlyIncre_w2 = np.nanmean(MatrixOnlyIncre[:,4])
AvgDecreOnlyIncre_w2 = np.nanmean(MatrixOnlyIncre[:,5])

NumIncre_axis = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32]
NumDecre_axis = [0, 1, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42]


auxFuncs.PlotCorrelationHeatmap(MatrixInVivo, AvgDecreInVivo_w1, AvgIncreInVivo_w1, AvgDecreInVivo_w2, AvgIncreInVivo_w2, NumDecre_axis, NumIncre_axis)
plt.savefig(folder + '/InVivoCorr.eps')
plt.close()
auxFuncs.PlotCorrelationHeatmap(MatrixOnlyIncre, AvgDecreOnlyIncre_w1, AvgIncreOnlyIncre_w1, AvgDecreOnlyIncre_w2, AvgIncreOnlyIncre_w2, NumDecre_axis, NumIncre_axis)
plt.savefig(folder + '/OnlyIncreCorr.eps')
plt.close()
auxFuncs.PlotCorrelationHeatmap(MatrixMirrorDecre, AvgDecreMirrorDecre_w1, AvgIncreMirrorDecre_w1, AvgDecreMirrorDecre_w2, AvgIncreMirrorDecre_w2, NumDecre_axis, NumIncre_axis)
plt.savefig(folder + '/MirrorDecreCorr.eps')
plt.close()
# auxFuncs.PlotCorrelationHeatmap(MatrixInVivo-MatrixMirrorDecre, AvgDecreMirrorDecre_w1, AvgIncreMirrorDecre_w1, AvgDecreMirrorDecre_w2, AvgIncreMirrorDecre_w2, NumDecre_axis, NumIncre_axis)
# plt.show()


