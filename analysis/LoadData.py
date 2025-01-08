import json
import glob
import numpy as np
import matplotlib.pyplot as plt
import pickle


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
    print(file,FileName)

    dataDict[FileName]={}

    SpikeTimes = np.array(data['simData']['spkt']).astype(float)
    SpikeIds = np.array(data['simData']['spkid']).astype(int)

    ####
    # Load FoxP2 spike times for each trial
    ####
    FoxP2 = [i for i in range(NumFoxP2)]
    Window = 1200
    StimTime = 1800
    SpikesList = []
    SpikeListPre = []
    SpikeListPost = []

    SpikeDecrePre = []
    SpikeDecrePost = []
    SpikeIncrePre = []
    SpikeIncrePost = []

    for i in FoxP2:
        Spiketimes = SpikeTimes[np.argwhere(SpikeIds == i).astype(int)].flatten()
        SpikesList.append(Spiketimes[abs(Spiketimes-StimTime) < Window])
        SpikeListPre.append(Spiketimes[(Spiketimes > StimTime-Window)*(Spiketimes < StimTime)])
        SpikeListPost.append(Spiketimes[(Spiketimes < StimTime+Window)*(Spiketimes > StimTime)])

        SpiketimesDecre = np.sort([s for i in data['net']['params']['popParams']['Decreasing_%d' % i]['spkTimes']
                                    for s in i])
        SpiketimesIncre = np.sort([s for i in data['net']['params']['popParams']['Increasing_%d' % i]['spkTimes']
                                    for s in i])

        SpikeDecrePre.append(SpiketimesDecre[(SpiketimesDecre > StimTime-Window)*(SpiketimesDecre < StimTime)])
        SpikeDecrePost.append(SpiketimesDecre[(SpiketimesDecre < StimTime+Window)*(SpiketimesDecre > StimTime)])
        SpikeIncrePre.append(SpiketimesIncre[(SpiketimesIncre > StimTime-Window)*(SpiketimesIncre < StimTime)])
        SpikeIncrePost.append(SpiketimesIncre[(SpiketimesIncre < StimTime+Window)*(SpiketimesIncre > StimTime)])

    SpikePre = np.array(SpikeListPre, dtype=object)
    SpikePost = np.array(SpikeListPost, dtype=object)

    SpikeDecrePre = np.array(SpikeDecrePre, dtype=object)
    SpikeDecrePost = np.array(SpikeDecrePost, dtype=object)

    SpikeIncrePre = np.array(SpikeIncrePre, dtype=object)
    SpikeIncrePost = np.array(SpikeIncrePost, dtype=object)

    RasterPre = bin_spikes(spike_times=SpikePre, dt=1, wdw_start=StimTime-Window, wdw_end=StimTime).transpose()
    RasterPost = bin_spikes(spike_times=SpikePost, dt=1, wdw_start=StimTime, wdw_end=StimTime+Window).transpose()

    RasterDecrePre = bin_spikes(spike_times=SpikeDecrePre, dt=1, wdw_start=StimTime-Window, wdw_end=StimTime).transpose()/NumDecreasing
    RasterDecrePost = bin_spikes(spike_times=SpikeDecrePost, dt=1, wdw_start=StimTime, wdw_end=StimTime+Window).transpose()/NumDecreasing

    RasterIncrePre = bin_spikes(spike_times=SpikeIncrePre, dt=1, wdw_start=StimTime-Window, wdw_end=StimTime).transpose()/NumIncreasing
    RasterIncrePost = bin_spikes(spike_times=SpikeIncrePost, dt=1, wdw_start=StimTime, wdw_end=StimTime+Window).transpose()/NumIncreasing

    # plt.imshow(RasterIncrePre, aspect='auto', interpolation='none')
    # plt.colorbar()
    # plt.show()
    # plt.imshow(RasterIncrePost, aspect='auto', interpolation='none')
    # plt.colorbar()
    # plt.show()
    # quit()

    dataDict[FileName]['SpikeTimes'] = np.array(SpikesList, dtype=object)
    dataDict[FileName]['PreOutputRate'] = RasterPre.mean()/(1/1000) # Convert to rate in Hz
    dataDict[FileName]['PostOutputRate'] = RasterPost.mean()/(1/1000) # Convert to rate in Hz
    dataDict[FileName]['PreDecreRate'] = RasterDecrePre.mean()/(1/1000) # Convert to rate in Hz
    dataDict[FileName]['PostDecreRate'] = RasterDecrePost.mean()/(1/1000) # Convert to rate in Hz
    dataDict[FileName]['PreIncreRate'] = RasterIncrePre.mean()/(1/1000) # Convert to rate in Hz
    dataDict[FileName]['PostIncreRate'] = RasterIncrePost.mean()/(1/1000) # Convert to rate in Hz

    print(dataDict[FileName]['PreOutputRate'], dataDict[FileName]['PostOutputRate'], dataDict[FileName]['PreDecreRate'],
          dataDict[FileName]['PostDecreRate'], dataDict[FileName]['PreIncreRate'], dataDict[FileName]['PostIncreRate'])

dataDict['keys'] = ('Condition', 'NumIncreasing', 'NumDecreasing', 'NumNotRelated', 'NetStimPre', 'NetStimPost',
                    'NetStimNoise', 'AMPAWeight', 'SynsPerConn')

with open("Sims_%s.pkl" % AMPA, 'wb') as f:
    pickle.dump(dataDict, f)