import numpy as np
import pickle
import matplotlib.pyplot as plt

formatFig = 'png'

for AMPAWeight in [0.0025, 0.005]:
    with open("Sims_%s.pkl" % AMPAWeight, 'rb') as f:
        data = pickle.load(f)
    del data['keys']
    for SynsPerConn in [1, 3]:
        RelevantSims = [i for i in data.keys() if int(i.split('_')[8]) == int(SynsPerConn)]
        NumIncreasing = []
        NumDecreasing = []
        PT5BDecre_preRate = []
        PT5BDecre_postRate = []
        PT5BIncre_preRate = []
        PT5BIncre_postRate = []
        FoxP2_preRate = []
        FoxP2_postRate = []
        Condition = []

        for i in RelevantSims:
            NumIncreasing.append(i.split('_')[1])
            NumDecreasing.append(i.split('_')[2])

            Condition.append(i.split('_')[0])

            PT5BDecre_preRate.append(data[i]['PreDecreRate'])
            PT5BDecre_postRate.append(data[i]['PostDecreRate'])

            PT5BIncre_preRate.append(data[i]['PreIncreRate'])
            PT5BIncre_postRate.append(data[i]['PostIncreRate'])

            FoxP2_preRate.append(data[i]['PreOutputRate'])
            FoxP2_postRate.append(data[i]['PostOutputRate'])

        NumIncreasing = np.array(NumIncreasing, dtype=int)
        NumDecreasing = np.array(NumDecreasing, dtype=int)
        Condition = np.array(Condition)

        PT5BDecre_preRate = np.array(PT5BDecre_preRate)
        PT5BDecre_postRate = np.array(PT5BDecre_postRate)

        PT5BIncre_preRate = np.array(PT5BIncre_preRate)
        PT5BIncre_postRate = np.array(PT5BIncre_postRate)

        FoxP2_preRate = np.array(FoxP2_preRate)
        FoxP2_postRate = np.array(FoxP2_postRate)

        ChosenIncre = int(18*5)
        ChosenDecre = int(51*5)

        maskIncre = np.argwhere(NumIncreasing == ChosenIncre).flatten()

        plt.figure(figsize=(12,10))
        for condition in np.unique(Condition):
            maskCondition = np.argwhere(Condition == condition).flatten()
            mask = np.intersect1d(maskIncre, maskCondition)
            sorted = np.argsort(NumDecreasing[mask])

            plt.subplot(2, 1, 1)
            plt.plot(NumDecreasing[mask][sorted]*PT5BDecre_preRate[mask][sorted],
                     FoxP2_preRate[mask][sorted],
                     label=str(condition)+' Pre-Cue PT5B Increasing rate %s Hz' % (int(ChosenIncre * PT5BIncre_preRate[mask][sorted].mean())))
            ax1 = plt.gca()
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            plt.xlim([10, 200])
            plt.xlabel('Pre-Cue PT5B Decreasing Rate (Hz)')
            plt.ylabel('Pre-Cue FoxP2 Mean Output Rate (Hz)')
            plt.subplot(2, 1, 2)
            plt.plot(NumDecreasing[mask][sorted]*PT5BDecre_postRate[mask][sorted],
                     FoxP2_postRate[mask][sorted],
                     label=str(condition) + ' Post-Cue PT5B Increasing rate %s Hz' % (
                                 int(ChosenIncre * PT5BIncre_postRate[mask][sorted].mean())))
            plt.xlabel('Post-Cue PT5B Decreasing Rate (Hz)')
            plt.ylabel('Post-Cue FoxP2 Mean Output Rate (Hz)')
            plt.xlim([10, 200])
            ax2 = plt.gca()
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
        ax1.legend(loc='upper right', frameon=False, fontsize=12)
        ax2.legend(loc='upper right', frameon=False, fontsize=12)
        plt.savefig("ComparingConditions_vsDecreasing_IO_%s_%s_Incre_%s_Decre_%s.%s" % (AMPAWeight, SynsPerConn, ChosenIncre, ChosenDecre, formatFig))

        maskDecre = np.argwhere(NumDecreasing == ChosenDecre).flatten()
        plt.figure(figsize=(12,10))
        for condition in np.unique(Condition):
            maskCondition = np.argwhere(Condition == condition).flatten()
            mask = np.intersect1d(maskDecre, maskCondition)
            sorted = np.argsort(NumIncreasing[mask])

            plt.subplot(2, 1, 1)
            plt.plot(NumIncreasing[mask][sorted]*PT5BIncre_preRate[mask][sorted],
                     FoxP2_preRate[mask][sorted],
                     label=str(condition)+' Pre-Cue PT5B Decreasing rate %s Hz' % (int(ChosenDecre * PT5BDecre_preRate[mask][sorted].mean())))
            ax1 = plt.gca()
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            plt.xlabel('Pre-Cue PT5B Increasing Rate (Hz)')
            plt.ylabel('Pre-Cue FoxP2 Mean Output Rate (Hz)')
            plt.subplot(2, 1, 2)
            plt.plot(NumIncreasing[mask][sorted]*PT5BIncre_preRate[mask][sorted],
                     FoxP2_postRate[mask][sorted],
                     label=str(condition) + ' Post-Cue PT5B Decreasing rate %s Hz' % (
                                 int(ChosenDecre * PT5BDecre_preRate[mask][sorted].mean())))
            plt.xlabel('Post-Cue PT5B Increasing Rate (Hz)')
            plt.ylabel('Post-Cue FoxP2 Mean Output Rate (Hz)')
            ax2 = plt.gca()
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
        ax1.legend(loc='upper right', frameon=False, fontsize=12)
        ax2.legend(loc='upper right', frameon=False, fontsize=12)
        plt.savefig("ComparingConditions_vsIncreasing_IO_%s_%s_Incre_%s_Decre_%s.%s" % (AMPAWeight, SynsPerConn, ChosenIncre, ChosenDecre, formatFig))


