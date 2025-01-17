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
TimeWindow1 = [1800, 2300]
TimeWindow2 = [2300, 2800]

AMPAWeight=0.001

MatrixInVivo, MatrixMirrorDecre, MatrixOnlyIncre = auxFuncs.CreateNeuronalArithmeticMatrix(df, TimeWindow1, TimeWindow2, AMPAWeight)
# Matrix has elements: NumIncreasing, NumDecreasing, DecRate in window1, IncRate in window1, FoxP2 in window1, and same for window2

AvgDecreasing1, AvgIncreasing1, AvgDecreasing2, AvgIncreasing2 = auxFuncs.CalculateAvgRatePerNeuron(MatrixInVivo)
AvgDecreasing1MirrorDecre, dummy, AvgDecreasing2MirrorDecre, dummyy = auxFuncs.CalculateAvgRatePerNeuron(MatrixMirrorDecre)
print(18*AvgIncreasing1, 51*AvgDecreasing1)

# auxFuncs.IO_rateVsPT5BIncre(MatrixInVivo, TimeWindowIndex=1)
# plt.savefig(folder+"/InVivoWindow1.eps")
# plt.close()
# auxFuncs.IO_rateVsPT5BIncre(MatrixInVivo, TimeWindowIndex=2)
# plt.savefig(folder+"/InVivoWindow2.eps")
# plt.close()
# auxFuncs.IO_rateVsPT5BIncre(MatrixMirrorDecre, TimeWindowIndex=1)
# plt.savefig(folder+"/MirrorDecreWindow1.eps")
# plt.close()
# auxFuncs.IO_rateVsPT5BIncre(MatrixMirrorDecre, TimeWindowIndex=2)
# plt.savefig(folder+"/MirrorDecreWindow2.eps")
# plt.close()
# auxFuncs.IO_rateVsPT5BIncre(MatrixOnlyIncre, TimeWindowIndex=1)
# plt.savefig(folder+"/OnlyIncreWindow1.eps")
# plt.close()
# auxFuncs.IO_rateVsPT5BIncre(MatrixOnlyIncre, TimeWindowIndex=2)
# plt.savefig(folder+"/OnlyIncreWindow2.eps")
# plt.close()


