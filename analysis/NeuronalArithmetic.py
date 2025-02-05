import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import auxFuncs

depolBlock = False
if depolBlock:
    folder = 'figuresNeuronalArithmeticDepol'
else:
    folder = 'figuresNeuronalArithmeticNoDepol'
df = pd.read_pickle("results/NeuronalArithmeticDepol%s.pkl" % depolBlock)

# Relevant time windows
TimeWindow1 = [1800-250, 1800+500]
TimeWindow2 = [1800+500, 1800+1250]
AMPAWeight=0.002
IncreList = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32]
DecreList = [0, 1, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42]

MatrixInVivo, MatrixMirrorDecre, MatrixOnlyIncre = auxFuncs.CreateNeuronalArithmeticMatrix(df, TimeWindow1,
                                                                                           TimeWindow2, AMPAWeight,
                                                                                           IncreList=IncreList,
                                                                                           DecreList=DecreList)

# Matrix has elements: NumIncreasing, NumDecreasing, DecRate in window1, IncRate in window1, FoxP2 in window1, and same for window2

AvgDecreasing1, AvgIncreasing1, AvgDecreasing2, AvgIncreasing2 = auxFuncs.CalculateAvgRatePerNeuron(MatrixInVivo)
AvgDecreasing1MirrorDecre, dummy, AvgDecreasing2MirrorDecre, dummyy = auxFuncs.CalculateAvgRatePerNeuron(MatrixMirrorDecre)

vmax=1800

auxFuncs.IO_rateVsPT5BIncre(MatrixInVivo, TimeWindowIndex=1, length=len(IncreList),
                            IncreList=IncreList, DecreList=DecreList, vmax=vmax)
plt.savefig(folder+"/InVivoWindow1.eps")
plt.close()
auxFuncs.IO_rateVsPT5BIncre(MatrixInVivo, TimeWindowIndex=2, vmax=vmax)
plt.savefig(folder+"/InVivoWindow2.eps")
plt.close()
auxFuncs.IO_rateVsPT5BIncre(MatrixMirrorDecre, TimeWindowIndex=1, vmax=vmax)
plt.savefig(folder+"/MirrorDecreWindow1.eps")
plt.close()
auxFuncs.IO_rateVsPT5BIncre(MatrixMirrorDecre, TimeWindowIndex=2, vmax=vmax)
plt.savefig(folder+"/MirrorDecreWindow2.eps")
plt.close()
auxFuncs.IO_rateVsPT5BIncre(MatrixOnlyIncre, TimeWindowIndex=1, vmax=vmax)
plt.savefig(folder+"/OnlyIncreWindow1.eps")
plt.close()
auxFuncs.IO_rateVsPT5BIncre(MatrixOnlyIncre, TimeWindowIndex=2, vmax=vmax)
plt.savefig(folder+"/OnlyIncreWindow2.eps")
plt.close()

auxFuncs.IO_gradientVsPT5BIncre(MatrixInVivo, TimeWindowIndex=1, length=len(IncreList),
                            IncreList=IncreList, DecreList=DecreList, vmax=vmax)
plt.savefig(folder+"/Gain_InVivoWindow1.eps")
plt.close()
auxFuncs.IO_gradientVsPT5BIncre(MatrixInVivo, TimeWindowIndex=2, vmax=vmax)
plt.savefig(folder+"/Gain_InVivoWindow2.eps")
plt.close()
auxFuncs.IO_gradientVsPT5BIncre(MatrixMirrorDecre, TimeWindowIndex=1, vmax=vmax)
plt.savefig(folder+"/Gain_MirrorDecreWindow1.eps")
plt.close()
auxFuncs.IO_gradientVsPT5BIncre(MatrixMirrorDecre, TimeWindowIndex=2, vmax=vmax)
plt.savefig(folder+"/Gain_MirrorDecreWindow2.eps")
plt.close()
auxFuncs.IO_gradientVsPT5BIncre(MatrixOnlyIncre, TimeWindowIndex=1, vmax=vmax)
plt.savefig(folder+"/Gain_OnlyIncreWindow1.eps")
plt.close()
auxFuncs.IO_gradientVsPT5BIncre(MatrixOnlyIncre, TimeWindowIndex=2, vmax=vmax)
plt.savefig(folder+"/Gain_OnlyIncreWindow2.eps")
plt.close()
