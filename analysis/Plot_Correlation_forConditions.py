import pickle
import time

import numpy as np
import matplotlib.pyplot as plt
import glob

AMPA = 0.0025
file = 'Correlation_Sims_%s.pkl' % AMPA

with open(file, 'rb') as f:
    data = pickle.load(f)

IncreConn = [int(18 * 0.5), 18, 18 * 2, 18 * 3, 18 * 4, 18 * 5]  # 25% Incre - 65% Decre
DecreConn = [int(51 * 0.5), 51, 51 * 2, 51 * 3, 51 * 4, 51 * 5]  #


ED_Matrix_1_InVivo = np.zeros((6,6))
ED_Matrix_3_InVivo = np.zeros((6,6))
ED_Matrix_1_OnlyIncre = np.zeros((6,6))
ED_Matrix_3_OnlyIncre = np.zeros((6,6))
ED_Matrix_1_MirrorDecre = np.zeros((6,6))
ED_Matrix_3_MirrorDecre = np.zeros((6,6))

del data['keys']

Variable = 'EuclideanDistance_FoxP2_Incre' # 'Correlation_FoxP2_Decre', 'Correlation_FoxP2_Incre',
                                           # 'EuclideanDistance_FoxP2_Decre', 'EuclideanDistance_FoxP2_Incre'

for filename in data.keys():
    Condition, NumIncreasing, NumDecreasing, NumNotRelated, NetStimPre, NetStimPost, NetStimNoise, AMPAWeight, \
    SynsPerConn = filename.split('_')
    IndexIncre = np.argwhere([i==int(NumIncreasing) for i in IncreConn]).flatten()[0]
    IndexDecre = np.argwhere([i==int(NumDecreasing) for i in DecreConn]).flatten()[0]

    if int(SynsPerConn)==1:
        if Condition=='InVivo':
            try:
                ED_Matrix_1_InVivo[IndexIncre,IndexDecre] = data[filename][Variable]
            except:
                ED_Matrix_1_InVivo[IndexIncre, IndexDecre] = data[filename][Variable].statistic
        elif Condition=='OnlyIncre':
            try:
                ED_Matrix_1_OnlyIncre[IndexIncre,IndexDecre] = data[filename][Variable]
            except:
                ED_Matrix_1_OnlyIncre[IndexIncre, IndexDecre] = data[filename][Variable].statistic
        elif Condition=='MirrorDecre':
            try:
                ED_Matrix_1_MirrorDecre[IndexIncre,IndexDecre] = data[filename][Variable]
            except:
                ED_Matrix_1_MirrorDecre[IndexIncre, IndexDecre] = data[filename][Variable].statistic
    else:
        if Condition=='InVivo':
            try:
                ED_Matrix_3_InVivo[IndexIncre,IndexDecre] = data[filename][Variable]
            except:
                ED_Matrix_3_InVivo[IndexIncre, IndexDecre] = data[filename][Variable].statistic
        elif Condition=='OnlyIncre':
            try:
                ED_Matrix_3_OnlyIncre[IndexIncre,IndexDecre] = data[filename][Variable]
            except:
                ED_Matrix_3_OnlyIncre[IndexIncre, IndexDecre] = data[filename][Variable].statistic
        elif Condition=='MirrorDecre':
            try:
                ED_Matrix_3_MirrorDecre[IndexIncre,IndexDecre] = data[filename][Variable]
            except:
                ED_Matrix_3_MirrorDecre[IndexIncre, IndexDecre] = data[filename][Variable].statistic


Min = 1
Max = 40

plt.imshow(ED_Matrix_1_InVivo, aspect='auto', interpolation='none', vmin=Min, vmax=Max)
plt.xlabel('Decreasing Rate')
plt.xticks([0,1,2,3,4,5], ['%1.0f' % (i*data[filename]['Decreasing_Rate_NotNorm'].mean()) for i in DecreConn])
plt.ylabel('Increasing Rate')
plt.yticks([0,1,2,3,4,5], ['%1.0f' % (i*data[filename]['Increasing_Rate_NotNorm'].mean()) for i in IncreConn])
plt.colorbar()
plt.savefig("DistanceBetwenFoxP2rateandPt5BIncre_InVivo.png")
plt.close()
plt.imshow(ED_Matrix_1_OnlyIncre, aspect='auto', interpolation='none', vmin=Min, vmax=Max)
plt.xlabel('Decreasing Rate')
plt.xticks([0,1,2,3,4,5], ['%1.0f' % (i*data[filename]['Decreasing_Rate_NotNorm'].mean()) for i in DecreConn])
plt.ylabel('Increasing Rate')
plt.yticks([0,1,2,3,4,5], ['%1.0f' % (i*data[filename]['Increasing_Rate_NotNorm'].mean()) for i in IncreConn])
plt.colorbar()
plt.savefig("DistanceBetwenFoxP2rateandPt5BIncre_OnlyIncre.png")
plt.close()
plt.imshow(ED_Matrix_1_MirrorDecre, aspect='auto', interpolation='none', vmin=Min, vmax=Max)
plt.xlabel('Decreasing Rate')
plt.xticks([0,1,2,3,4,5], ['%1.0f' % (i*data[filename]['Decreasing_Rate_NotNorm'].mean()) for i in DecreConn])
plt.ylabel('Increasing Rate')
plt.yticks([0,1,2,3,4,5], ['%1.0f' % (i*data[filename]['Increasing_Rate_NotNorm'].mean()) for i in IncreConn])
plt.colorbar(label=Variable)
plt.savefig("DistanceBetwenFoxP2rateandPt5BIncre_MirrorDecre.png")
plt.close()
