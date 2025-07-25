# Load simulations
import json
import glob
import numpy as np
import pickle

DepolBlock=False

folder = '../data/gridsearch_Dep%s' % DepolBlock

files = sorted(glob.glob(folder + '/*_data.json'))

dataDict = {}

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)

    [print(i) for i in data['simConfig']]
    quit()
    NumFoxP2 = data['simConfig']['numTrials']
    NumIncreasing = data['simConfig']['IncreConn']
    NumDecreasing = data['simConfig']['DecreConn']
    NumNotRelated = data['simConfig']['NotChangingConn']
    Condition = data['simConfig']['Condition'].split('_')[0]
    AMPAWeight = data['simConfig']['AMPA_weight'] # AMPA weight for all 3 populations are the same
    NetStimNoise = data['simConfig']['NetStimNoise']
    NoisePresent = data['simConfig']['NoiseMultiplier']==1
    NetStimPre = data['simConfig']['NetStimRatePre']
    NetStimPost = data['simConfig']['NetStimRatePost']
    SynsPerConn = data['simConfig']['synsPerConn']
    IAmp = data['simConfig']['IAmp']

    FileName = '%s_%d_%d_%d_%s_%s_%s_%s_%s_%s_%s' % (Condition, NumIncreasing, NumDecreasing, NumNotRelated, NetStimPre,
                                               NetStimPost, NetStimNoise, AMPAWeight, SynsPerConn, IAmp, NoisePresent)
    print(file,FileName)

    dataDict[FileName]={}

    SpikeTimes = np.array(data['simData']['spkt']).astype(float)
    SpikeIds = np.array(data['simData']['spkid']).astype(int)

    ####
    # Load FoxP2 spike times for each trial
    ####
    FoxP2 = [i for i in range(NumFoxP2)]

    SpikesList = []
    SpikeDecre = []
    SpikeIncre = []
    SpikeBackground = []

    for i in FoxP2:
        Spiketimes = SpikeTimes[np.argwhere(SpikeIds == i).astype(int)].flatten()
        SpikesList.append(Spiketimes)

        # Concatenate all input spikes per trial
        try:
            SpiketimesDecre = np.sort([s for i in data['net']['pops']['Decreasing_%d' % i]['tags']['spkTimes']
                                        for s in i])
        except:
            SpiketimesDecre = []
        try:
            SpiketimesIncre = np.sort([s for i in data['net']['pops']['Increasing_%d' % i]['tags']['spkTimes']
                                        for s in i])
        except:
            SpiketimesIncre = []

        try:
            SpiketimesBackground = np.sort([i for i in data['net']['pops']['ExtraInputs_%d' % i]['tags']['spkTimes']])
        except:
            SpiketimesBackground = []

        SpikeDecre.append(SpiketimesDecre)
        SpikeIncre.append(SpiketimesIncre)
        SpikeBackground.append(SpiketimesBackground)

    SpikeFoxP2 = np.array(SpikesList, dtype=object)
    SpikeDecre = np.array(SpikeDecre, dtype=object)
    SpikeIncre = np.array(SpikeIncre, dtype=object)
    SpikeBackground = np.array(SpikeBackground, dtype=object)

    dataDict[FileName]['SpikeFoxP2'] = SpikeFoxP2
    dataDict[FileName]['SpikeDecre'] = SpikeDecre
    dataDict[FileName]['SpikeIncre'] = SpikeIncre
    dataDict[FileName]['SpikeBackground'] = SpikeBackground

    Impedance = []
    Time = []
    for key, value in data['simData']['Impedance'].items():
        Impedance.append(value)
        Time.append(float(key))
    Impedance = np.array(Impedance)
    Time = np.array(Time)

    dataDict[FileName]['Impedance']={}
    dataDict[FileName]['Impedance']['Value'] = Impedance
    dataDict[FileName]['Impedance']['Time'] = Time

with open("results/SimSpikesDepol%s.pkl" % DepolBlock, 'wb') as f:
    pickle.dump(dataDict, f)