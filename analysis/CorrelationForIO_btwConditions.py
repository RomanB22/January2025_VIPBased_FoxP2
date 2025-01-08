import json
import glob
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy import ndimage
from scipy import signal
import math
from scipy.stats import pearsonr
import time

def bin_spikes(spike_times, dt, wdw_start, wdw_end):
    # Function that puts spikes into bins
    edges = np.arange(wdw_start, wdw_end, dt)  # Get edges of time bins
    num_bins = edges.shape[0] - 1  # Number of bins
    num_neurons = spike_times.shape[0]  # Number of neurons
    neural_data = np.empty([num_bins, num_neurons])  # Initialize array for binned neural data
    # Count number of spikes in each bin for each neuron, and put in array
    for i in range(num_neurons):
        neural_data[:, i] = np.histogram(spike_times[i], edges)[0]
    return neural_data

def overlapping_window(np_array, window_size=50):
    return ndimage.uniform_filter1d(np_array, size=window_size, axis=1, mode='constant')

def non_overlapping_window(np_array, window_size=50):
    window_hop = window_size
    start_frame = window_size
    end_frame = window_hop * math.floor(float(np_array.shape[1]) / window_hop)
    window = []
    for frame_idx in range(start_frame, end_frame, window_hop):
        window.append(np.mean(np_array[:, frame_idx - window_size:frame_idx],  axis=1)) # Add mean

    return np.transpose(np.vstack(window))

AMPA=0.0025
folder = '../data/grid_search_%s_False' % AMPA
files = glob.glob(folder + '/*.json')
dataDict = {}

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)

    NumFoxP2 = data['simConfig']['numTrials']
    NumIncreasing = data['simConfig']['IncreConn']
    NumDecreasing = data['simConfig']['DecreConn']
    NumNotRelated = data['simConfig']['NotChangingConn']
    Condition = data['simConfig']['Condition'].split('_')[0]
    AMPAWeight = data['simConfig']['AMPANMDAWeightsDecre'] # g_AMPA for all 3 populations are the same
    NetStimNoise = data['simConfig']['NetStimNoise']
    NetStimPre = data['simConfig']['NetStimRatePre']
    NetStimPost = data['simConfig']['NetStimRatePost']
    SynsPerConn = data['simConfig']['synsPerConn']

    FileName = '%s_%d_%d_%d_%s_%s_%s_%s_%s' % (Condition, NumIncreasing, NumDecreasing, NumNotRelated, NetStimPre,
                                               NetStimPost, NetStimNoise, AMPAWeight, SynsPerConn)

    dataDict[FileName]={}

    SpikeTimes = np.array(data['simData']['spkt']).astype(float)
    SpikeIds = np.array(data['simData']['spkid']).astype(int)

    ####
    # Load FoxP2 spike times for each trial
    ####
    FoxP2 = [i for i in range(NumFoxP2)]
    Window = 1800
    StimTime = 1800
    smoothingWindow = 100
    SpikesList = []
    SpikeDecre = []
    SpikeIncre = []


    for i in FoxP2:
        Spiketimes = SpikeTimes[np.argwhere(SpikeIds == i).astype(int)].flatten()
        SpikesList.append(Spiketimes[abs(Spiketimes-StimTime) < Window])

        SpiketimesDecre = np.sort([s for i in data['net']['params']['popParams']['Decreasing_%d' % i]['spkTimes']
                                    for s in i])
        SpiketimesIncre = np.sort([s for i in data['net']['params']['popParams']['Increasing_%d' % i]['spkTimes']
                                    for s in i])

        SpikeDecre.append(SpiketimesDecre[abs(SpiketimesDecre-StimTime) < Window])
        SpikeIncre.append(SpiketimesIncre[abs(SpiketimesIncre-StimTime) < Window])

    Spike = np.array(SpikesList, dtype=object)
    SpikeDecre = np.array(SpikeDecre, dtype=object)
    SpikeIncre = np.array(SpikeIncre, dtype=object)
    # Normalize by Number of inputs or not? For now just look at correlation with normalized inputs
    windowStart=StimTime
    windowEnd=StimTime+int(Window/2.)
    RasterFoxP2 = overlapping_window(bin_spikes(spike_times=Spike, dt=1, wdw_start=windowStart,
                                                wdw_end=windowEnd).transpose(),
                                     window_size=smoothingWindow).mean(axis=0)/(1/1000)
    RasterDecre = overlapping_window(bin_spikes(spike_times=SpikeDecre, dt=1, wdw_start=windowStart,
                                                wdw_end=windowEnd).transpose(),
                                     window_size=smoothingWindow).mean(axis=0)/(1/1000)#/NumDecreasing
    RasterIncre = overlapping_window(bin_spikes(spike_times=SpikeIncre, dt=1, wdw_start=windowStart,
                                                wdw_end=windowEnd).transpose(),
                                     window_size=smoothingWindow).mean(axis=0)/(1/1000)#/NumIncreasing

    RasterFoxP2NotNorm = RasterFoxP2[int(smoothingWindow / 2):-int(smoothingWindow / 2)]
    RasterDecreNotNorm = RasterDecre[int(smoothingWindow / 2):-int(smoothingWindow / 2)]
    RasterIncreNotNorm = RasterIncre[int(smoothingWindow / 2):-int(smoothingWindow / 2)]

    RasterFoxP2 = (RasterFoxP2NotNorm-np.mean(RasterFoxP2NotNorm))/np.std(RasterFoxP2NotNorm)
    RasterDecre = (RasterDecreNotNorm-np.mean(RasterDecreNotNorm))/np.std(RasterDecreNotNorm)
    RasterIncre = (RasterIncreNotNorm-np.mean(RasterIncreNotNorm))/np.std(RasterIncreNotNorm)

    # plt.imshow(RasterFoxP2, aspect='auto', interpolation='none')
    # plt.colorbar()
    # plt.show()
    # plt.imshow(RasterDecre, aspect='auto', interpolation='none')
    # plt.colorbar()
    # plt.show()
    # plt.imshow(RasterIncre, aspect='auto', interpolation='none')
    # plt.colorbar()
    # plt.show()
    # quit()
    plt.plot(RasterFoxP2, label='FoxP2')
    plt.plot(RasterDecre, label='Decre')
    plt.plot(RasterIncre, label='Incre')
    plt.legend()
    # plt.show()
    plt.savefig('./NormalizedFR/'+FileName+'.png')
    plt.close()
    # time.sleep(3)

    resDecre = pearsonr(RasterDecre, RasterFoxP2, axis=0)
    resIncre = pearsonr(RasterIncre, RasterFoxP2, axis=0)
    ED_Decre = np.linalg.norm(RasterDecre-RasterFoxP2)
    ED_Incre = np.linalg.norm(RasterIncre-RasterFoxP2)

    # print(FileName)
    print(FileName.split('_')[0], "Decre:", NumDecreasing, "Incre:", NumIncreasing,
          "Decre-FoxP2 distance:", ED_Decre, "Incre-FoxP2 distance:", ED_Incre)
    # time.sleep(3)

    dataDict[FileName]['FoxP2_Rate'] = RasterFoxP2
    dataDict[FileName]['Decreasing_Rate'] = RasterDecre
    dataDict[FileName]['Increasing_Rate'] = RasterIncre

    dataDict[FileName]['FoxP2_Rate_NotNorm'] = RasterFoxP2NotNorm
    dataDict[FileName]['Decreasing_Rate_NotNorm'] = RasterDecreNotNorm/NumDecreasing
    dataDict[FileName]['Increasing_Rate_NotNorm'] = RasterIncreNotNorm/NumIncreasing

    dataDict[FileName]['Correlation_FoxP2_Decre'] = resDecre
    dataDict[FileName]['Correlation_FoxP2_Incre'] = resIncre
    dataDict[FileName]['EuclideanDistance_FoxP2_Decre'] = ED_Decre
    dataDict[FileName]['EuclideanDistance_FoxP2_Incre'] = ED_Incre

    # print(dataDict[FileName]['FoxP2_Rate'], dataDict[FileName]['Decreasing_Rate'], dataDict[FileName]['Increasing_Rate'])

dataDict['keys'] = ('Condition', 'NumIncreasing', 'NumDecreasing', 'NumNotRelated', 'NetStimPre', 'NetStimPost',
                    'NetStimNoise', 'AMPAWeight', 'SynsPerConn')

with open("Correlation_Sims_%s.pkl" % AMPA, 'wb') as f:
    pickle.dump(dataDict, f)
