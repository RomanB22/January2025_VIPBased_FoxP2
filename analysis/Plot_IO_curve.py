import numpy as np
import pickle
import matplotlib.pyplot as plt

def plotIO(ParameterVariable, ControlVariable, XMultiplier, YMultiplier, Output, title='Post Cue IO response',
           xlabel='#Increasing PT5B', xlim=[0, 350], ylim=[0, 280],
           ylabel='Post Cue FoxP2 Mean Output Rate (Hz)', legendLabel='#Decreasing PT5B = %d'):
    n = len(np.unique(ParameterVariable))
    colors = plt.cm.viridis(np.linspace(0, 1, n))
    i=0
    for decreCell in np.unique(ParameterVariable):
        # print(decreCell)
        mask = ParameterVariable == decreCell
        X = ControlVariable[mask] * XMultiplier[mask]
        Y = Output[mask]
        order = np.argsort(X)
        plt.plot(X[order], Y[order], '-', label=legendLabel % (decreCell * YMultiplier[mask].mean()), color=colors[i])
        if i==1:
            plt.plot(X[order][1], Y[order][1], '*', color='tab:red', markersize=15, label='Experimental mean parameters')
        plt.title(title)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # plt.xlim(xlim)
        # plt.ylim(ylim)
        i+=1
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left', bbox_to_anchor=(1.05, 1), frameon=False, fontsize=12)

formatFig = 'png'

for AMPAWeight in [0.0025, 0.005]:
    # The OnlyIncre condition will be the "control", assuming that the relevant info is carried by the OnlyIncre
    # The second point in all plots corresponds to the experimental proportion (in theory)
    for Condition in ['InVivo', 'MirrorDecre', 'OnlyIncre']:
        for SynsPerConn in [1,3]:

            with open("Sims_%s.pkl" % AMPAWeight, 'rb') as f:
                data = pickle.load(f)

            # print(data.keys())
            # Filename of sims has the following info: ('Condition', 'NumIncreasing', 'NumDecreasing', 'NumNotRelated',
            # 'NetStimPre', 'NetStimPost', 'NetStimNoise', 'AMPAWeight', 'SynsPerConn')

            RelevantSims = [i for i in data.keys() if (i.split('_')[0] == Condition and int(i.split('_')[8]) == int(SynsPerConn))]
            NumIncreasing = []
            NumDecreasing = []
            PT5BDecre_preRate = []
            PT5BDecre_postRate = []
            PT5BIncre_preRate = []
            PT5BIncre_postRate = []
            FoxP2_preRate = []
            FoxP2_postRate = []

            for i in RelevantSims:
                NumIncreasing.append(i.split('_')[1])
                NumDecreasing.append(i.split('_')[2])

                PT5BDecre_preRate.append(data[i]['PreDecreRate'])
                PT5BDecre_postRate.append(data[i]['PostDecreRate'])

                PT5BIncre_preRate.append(data[i]['PreIncreRate'])
                PT5BIncre_postRate.append(data[i]['PostIncreRate'])

                FoxP2_preRate.append(data[i]['PreOutputRate'])
                FoxP2_postRate.append(data[i]['PostOutputRate'])

            NumIncreasing = np.array(NumIncreasing, dtype=int)
            NumDecreasing = np.array(NumDecreasing, dtype=int)

            PT5BDecre_preRate = np.array(PT5BDecre_preRate)
            PT5BDecre_postRate = np.array(PT5BDecre_postRate)

            PT5BIncre_preRate = np.array(PT5BIncre_preRate)
            PT5BIncre_postRate = np.array(PT5BIncre_postRate)

            FoxP2_preRate = np.array(FoxP2_preRate)
            FoxP2_postRate = np.array(FoxP2_postRate)

            def plotFigure1():
                plt.figure(figsize=(10, 12))
                ParameterVariable = NumDecreasing
                ControlVariable = NumIncreasing
                XMultiplier, YMultiplier = PT5BIncre_preRate, PT5BDecre_preRate
                Output = FoxP2_preRate
                title= None #'Pre Cue IO response - %s condition' % Condition
                # plt.subplot(3, 1, 1)
                plt.subplot(2, 1, 1)
                plotIO(ParameterVariable, ControlVariable, XMultiplier, YMultiplier, Output, title=title,
                       xlabel='Pre-Cue PT5B Increasing Rate (Hz)', ylabel='Pre-Cue Mean Output Rate (Hz)',
                       legendLabel='Pre-Cue PT5B Decreasing Rate = %d Hz', xlim=[0, 150], ylim=[0, 280])

                XMultiplier, YMultiplier = PT5BIncre_postRate, PT5BDecre_postRate
                Output = FoxP2_postRate
                title= None#'Post Cue IO response - %s condition' % Condition
                # plt.subplot(3, 1, 1)
                plt.subplot(2, 1, 2)
                plotIO(ParameterVariable, ControlVariable, XMultiplier, YMultiplier, Output, title=title, xlabel='Post-Cue PT5B Increasing Rate (Hz)',
                           ylabel='Post-Cue Mean Output Rate (Hz)', legendLabel='Post-Cue PT5B Decreasing Rate = %d Hz')

                # Output = FoxP2_postRate-FoxP2_preRate
                # title= None#'Post-Pre Cue IO response'
                # plt.subplot(3, 1, 3)
                # plotIO(ParameterVariable, ControlVariable, Output, title=title, xlabel='PT5B Increasing Rate (Hz)',
                #            ylabel='$\Delta$Output Rate (Hz)', legendLabel='PT5B Decreasing Rate = %d')
                plt.tight_layout()
                plt.savefig('%s_IO_vs_Increasing_PT5B_AMPA%s_SynsPerConn%s.%s' % (Condition, AMPAWeight, SynsPerConn, formatFig))
                plt.close()
                # plt.show()


            def plotFigure2():
                plt.figure(figsize=(10, 12))
                ParameterVariable = NumIncreasing
                ControlVariable = NumDecreasing
                XMultiplier, YMultiplier = PT5BDecre_preRate, PT5BIncre_preRate
                Output = FoxP2_preRate
                title = None #'Pre Cue IO response - %s condition' % Condition
                # plt.subplot(3, 1, 1)
                plt.subplot(2, 1, 1)
                plotIO(ParameterVariable, ControlVariable, XMultiplier, YMultiplier, Output, title=title,
                       xlabel='Pre-Cue PT5B Decreasing Rate (Hz)', ylabel='Pre-Cue Mean Output Rate (Hz)',
                       legendLabel='Pre-Cue PT5B Increasing Rate = %d Hz', xlim=[0, 150], ylim=[0, 280])

                XMultiplier, YMultiplier = PT5BDecre_postRate, PT5BIncre_postRate
                Output = FoxP2_postRate
                title = 'Post Cue IO response - %s condition' % Condition
                # plt.subplot(3, 1, 2)
                plt.subplot(2, 1, 2)
                plotIO(ParameterVariable, ControlVariable, XMultiplier, YMultiplier, Output, title=title, xlabel='Post-Cue PT5B Decreasing Rate (Hz)',
                       ylabel='Post-Cue Mean Output Rate (Hz)', legendLabel='Post-Cue PT5B Increasing Rate = %d Hz')

                # Output = FoxP2_postRate - FoxP2_preRate
                # title = None  # 'Post-Pre Cue IO response'
                # plt.subplot(3, 1, 3)
                # plotIO(ParameterVariable, ControlVariable, Output, title=title, xlabel='PT5B Decreasing Rate (Hz)',
                #        ylabel='$\Delta$Output Rate (Hz)', legendLabel='PT5B Increasing Rate = %d')
                plt.tight_layout()
                plt.savefig('%s_IO_vs_Decreasing_PT5B_AMPA%s_SynsPerConn%s.%s' % (Condition, AMPAWeight, SynsPerConn, formatFig))
                plt.close()
                # plt.show()

            plotFigure1()
            plotFigure2()