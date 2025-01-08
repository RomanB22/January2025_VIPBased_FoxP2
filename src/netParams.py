from netpyne.batchtools import specs
from src.cfg import cfg
import pickle
import random
import numpy as np
import json

cfg.update_cfg()
### params ###
# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters
netParams.defaultThreshold = -10.0
netParams.defineCellShapes = True       # sets 3d geometry aligned along the y-axis
netParams.version = 1
###############################################################################
## Cell types
###############################################################################
cellLabel = 'FoxP2'
cellType = {'cellType': 'FoxP2', 'cellModel': 'HH_reduced'}

cellRule = netParams.importCellParams(label='FoxP2', conds={'cellType': 'FoxP2', 'cellModel': 'HH_reduced'},
                                      fileName='cells/vipcr_cell.hoc', cellName='FoxP2', importSynMechs=True)

tunedParams = {
            "ori1": {
                "Nafcr": {
                    "gnafbar": 0.02947620800082492
                },
                "Ra": 66.17717073966959,
                "cm": 0.8606517206570653,
                "kdrcr": {
                    "gkdrbar": 0.006481906573492726
                },
                "pas": {
                    "e": -33.49027694823483,
                    "g": 5.284515381280852e-06
                }
            },
            "ori2": {
                "Nafcr": {
                    "gnafbar": 0.018286391443029005
                },
                "Ra": 159.4874720208395,
                "cm": 1.7871266049926409,
                "kdrcr": {
                    "gkdrbar": 0.016523904347241908
                },
                "pas": {
                    "e": -41.34129067194086,
                    "g": 1.2845832582194357e-05
                }
            },
            "rad1": {
                "Nafcr": {
                    "gnafbar": 0.07030555623892656
                },
                "Ra": 146.97264222491765,
                "cm": 3.4665873634587534,
                "kdrcr": {
                    "gkdrbar": 0.018420121447432505
                },
                "pas": {
                    "e": -63.7255765480871,
                    "g": 0.0001323517375006819
                }
            },
            "rad2": {
                "Nafcr": {
                    "gnafbar": 0.10815212950869402
                },
                "Ra": 131.1200150750147,
                "cm": 1.614263133932052,
                "kdrcr": {
                    "gkdrbar": 0.011784330166693467
                },
                "pas": {
                    "e": -76.90504975769215,
                    "g": 5.373327212183193e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.006783930646116449
                },
                "Nafcr": {
                    "gnafbar": 0.007947914708069291
                },
                "Ra": 148.34549887491144,
                "cancr": {
                    "gcabar": 0.009161468313502903
                },
                "cm": 2.1218785384646157,
                "iCcr": {
                    "gkcbar": 0.0001241181978117609
                },
                "kdrcr": {
                    "gkdrbar": 0.011182089978118509
                },
                "pas": {
                    "e": -74.47383900052466,
                    "g": 5.0861905608848625e-06
                }
            }
        }

cellRule['secs']['soma']['mechs']['Nafcr']['gnafbar'] = tunedParams['soma']['Nafcr']['gnafbar']
cellRule['secs']['soma']['mechs']['kdrcr']['gkdrbar'] = tunedParams['soma']['kdrcr']['gkdrbar']
cellRule['secs']['soma']['mechs']['IKscr']['gKsbar'] = tunedParams['soma']['IKscr']['gKsbar']
cellRule['secs']['soma']['mechs']['iCcr']['gkcbar'] = tunedParams['soma']['iCcr']['gkcbar']
cellRule['secs']['soma']['mechs']['cancr']['gcabar'] = tunedParams['soma']['cancr']['gcabar']
cellRule['secs']['soma']['mechs']['pas']['e'] = tunedParams['soma']['pas']['e']
cellRule['secs']['soma']['geom']['cm'] = tunedParams['soma']['cm']
cellRule['secs']['soma']['geom']['Ra'] = tunedParams['soma']['Ra']
cellRule['secs']['soma']['mechs']['pas']['g'] = tunedParams['soma']['pas']['g']

for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
    cellRule['secs'][sec]['mechs']['Nafcr']['gnafbar'] = tunedParams[sec]['Nafcr']['gnafbar']
    cellRule['secs'][sec]['mechs']['kdrcr']['gkdrbar'] = tunedParams[sec]['kdrcr']['gkdrbar']
    cellRule['secs'][sec]['mechs']['pas']['e'] = tunedParams[sec]['pas']['e']
    cellRule['secs'][sec]['geom']['cm'] = tunedParams[sec]['cm']
    cellRule['secs'][sec]['geom']['Ra'] = tunedParams[sec]['Ra']
    cellRule['secs'][sec]['mechs']['pas']['g'] = tunedParams[sec]['pas']['g']

cellRule['secLists']['dendList'] = ['rad1', 'rad2', 'ori1', 'ori2']

#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
netParams.synMechParams['NMDA'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': 2, 'tau2NMDA': 100, 'e': 0}
netParams.synMechParams['AMPA'] = {'mod': 'MyExp2SynBB', 'tau1': cfg.tau1, 'tau2': cfg.tau2, 'e': 0}

# ------------------------------------------------------------------------------
# VecStim inputs
# ------------------------------------------------------------------------------

def BagOfSpikeTimes(Results, RandomRealization='Random_0', Condition='InVivo_Go'):
    # Make a big bag of spikeTimes
    sampledNeuronsIncre = {}
    sampledNeuronsDecre = {}
    sampledNeuronsNotChanging = {}

    for trial in Results[Condition].keys():
        for cell in Results[Condition][trial].keys():
            if cell.startswith('Cell_'):
                ID = Results[Condition][trial][cell]['ID']
                spkTimes = Results[Condition][trial][cell]['SimSpks'][RandomRealization]
                if ID=='Increasing':
                    sampledNeuronsIncre[ID+'_'+cell+'_'+trial]=spkTimes
                elif ID=='Decreasing':
                    sampledNeuronsDecre[ID + '_' + cell + '_' + trial] = spkTimes
                elif ID=='Not Changing':
                    sampledNeuronsNotChanging[ID + '_' + cell + '_' + trial] = spkTimes

    return sampledNeuronsIncre, sampledNeuronsDecre, sampledNeuronsNotChanging

def SampleSpikeTrains(SimulatedSpikes, numNeurons, numTrials):
    import random
    sampledKeys = []
    spikeTimes = []
    for trial in range(numTrials):
        # In each trial I don't repeat cells nor trials, but there could be repetition of some cells between trials
        randomKeys=random.sample(list(SimulatedSpikes.keys()), numNeurons)
        sampledKeys.append(randomKeys)
        sampledSpikes = [SimulatedSpikes[i] for i in randomKeys]
        spikeTimes.append(sampledSpikes)

    return sampledKeys, spikeTimes

if cfg.addVecStim:
    ####
    # Load the spike trains
    if cfg.GoNoGo == 'Go':
        with open('cells/Results_Go.pkl', 'rb') as results:
            Results = pickle.load(results)
    elif cfg.GoNoGo == 'NoGo':
        with open('cells/Results_NoGo.pkl', 'rb') as results:
            Results = pickle.load(results)

    AllNeuronsIncre, AllNeuronsDecre, AllNeuronsNotChanging = BagOfSpikeTimes(Results, Condition=cfg.Condition)

    sampledNeuronsIncre, spikeTimesIncre = SampleSpikeTrains(AllNeuronsIncre, numNeurons=cfg.IncreConn,
                                                             numTrials=cfg.numTrials)
    sampledNeuronsDecre, spikeTimesDecre = SampleSpikeTrains(AllNeuronsDecre, numNeurons=cfg.DecreConn,
                                                             numTrials=cfg.numTrials)
    sampledNeuronsNotChanging, spikeTimesNotChanging = SampleSpikeTrains(AllNeuronsNotChanging,
                                                                         numNeurons=cfg.NotChangingConn,
                                                                         numTrials=cfg.numTrials)
    # # We can save the sampled neurons if we want to. If running batch will overwrite
    # with open(cfg.saveFolder+cfg.simLabel+f"/Increasing_{cfg.Condition}_{cfg.IncreConn}_{cfg.DecreConn}", 'w') as file:
    #     json.dump(sampledNeuronsIncre, file, indent=4)
    # # We can save the sampled neurons if we want to
    # with open(cfg.saveFolder+cfg.simLabel+f"/Decreasing_{cfg.Condition}_{cfg.IncreConn}_{cfg.DecreConn}", 'w') as file:
    #     json.dump(sampledNeuronsDecre, file, indent=4)
    # # We can save the sampled neurons if we want to
    # with open(cfg.saveFolder+cfg.simLabel+f"/NotChanging_{cfg.Condition}_{cfg.IncreConn}_{cfg.DecreConn}", 'w') as file:
    #     json.dump(sampledNeuronsNotChanging, file, indent=4)

    netParams.popParams['FoxP2'] = {'cellModel': 'HH_reduced', 'cellType': 'FoxP2', 'numCells': cfg.numTrials}

    for Trial in range(cfg.numTrials):
        spikeTimesIncreTrial = spikeTimesIncre[Trial]
        spikeTimesDecreTrial = spikeTimesDecre[Trial]
        spikeTimesNotChangingTrial = spikeTimesNotChanging[Trial]
        ### Define Populations
        netParams.popParams[f'Increasing_{Trial}'] = {'cellModel': 'VecStim',
                                                      'numCells': len(spikeTimesIncreTrial),
                                                      'spkTimes': spikeTimesIncreTrial}
        netParams.popParams[f'Decreasing_{Trial}'] = {'cellModel': 'VecStim',
                                                      'numCells': len(spikeTimesDecreTrial),
                                                      'spkTimes': spikeTimesDecreTrial}
        netParams.popParams[f'NotChanging_{Trial}'] = {'cellModel': 'VecStim',
                                                       'numCells': len(spikeTimesNotChangingTrial),
                                                       'spkTimes': spikeTimesNotChangingTrial}
        Weights = {'Increasing': cfg.AMPANMDAWeightsIncre, 'Decreasing': cfg.AMPANMDAWeightsDecre,
                   'NotChanging': cfg.AMPANMDAWeightsNotChanging}

    ####
    # Connect them
    PT5Bpops = [i for i in netParams.popParams.keys() if i != 'FoxP2']

    for InputPops in PT5Bpops:
        connection = f'{InputPops}->FoxP2_%d' % int(InputPops.split('_')[1])
        numPreSyn = netParams.popParams[InputPops]['numCells']
        preSynSoma = np.sort(random.sample([i for i in range(numPreSyn)], int(cfg.somaProb * numPreSyn)))
        preSynDend = np.sort([i for i in range(numPreSyn) if i not in preSynSoma])
        secList = random.sample(['rad1', 'rad2', 'ori1', 'ori2']*len(preSynDend), len(preSynDend))

        netParams.connParams[connection + '_soma'] = {
            'preConds': {'popLabel': InputPops},
            'postConds': {'popLabel': 'FoxP2'},
            'weight': Weights[InputPops.split('_')[0]],
            'sec': 'soma',
            'synsPerConn': cfg.synsPerConn,
            'connList': [[i, int(InputPops.split('_')[1])] for i in preSynSoma],
            'delay': cfg.delay,
            'loc': 0.5,
            'synMech': cfg.ESynMech}

        netParams.connParams[connection + '_dend'] = {
            'preConds': {'popLabel': InputPops},
            'postConds': {'popLabel': 'FoxP2'},
            'weight': Weights[InputPops.split('_')[0]],
            'synsPerConn': cfg.synsPerConn,
            'sec': secList,
            'connList': [[i, int(InputPops.split('_')[1])] for i in preSynDend],
            'delay': cfg.delay,
            'loc': 'uniform(0,0.8)',
            'synMech': cfg.ESynMech}

else:
    netParams.popParams['FoxP2'] = {'cellModel': 'HH_reduced', 'cellType': 'FoxP2', 'numCells': 1}

# ------------------------------------------------------------------------------
# NetStim inputs
# ------------------------------------------------------------------------------
if cfg.addNetStim:
    # add stim source
    netParams.stimSourceParams['ExtraInputsPre'] = {'type': 'NetStim', 'start': 0,
                                                    'dur': cfg.duration / 2, 'interval': 1000 / cfg.NetStimRatePre,
                                                    'noise': cfg.NetStimNoise, 'number': cfg.NetStimNumber}
    netParams.stimSourceParams['ExtraInputsPos'] = {'type': 'NetStim', 'start': cfg.duration / 2,
                                                    'dur': cfg.duration / 2, 'interval': 1000 / cfg.NetStimRatePost,
                                                    'noise': cfg.NetStimNoise, 'number': cfg.NetStimNumber}
    # connect stim source to target
    netParams.stimTargetParams['ExtraInputsPre_FoxP2'] = {
        'source': 'ExtraInputsPre',
        'conds': {'popLabel': 'FoxP2'},
        'synsPerConn': cfg.synsPerConn,
        'sec': 'soma',
        'loc': 0.5,
        'synMech': cfg.ESynMech,
        'weight': cfg.NetStimWeight,
        'delay': cfg.NetStimDelay}

    # connect stim source to target
    netParams.stimTargetParams['ExtraInputsPos_FoxP2'] = {
        'source': 'ExtraInputsPos',
        'conds': {'popLabel': 'FoxP2'},
        'synsPerConn': cfg.synsPerConn,
        'sec': 'soma',  # dend y soma?
        'loc': 0.5,
        'synMech': cfg.ESynMech,
        'weight': cfg.NetStimWeight,
        'delay': cfg.NetStimDelay}

#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
     for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params
        amps = ic['amp'] if isinstance(ic['amp'], list) else [ic['amp']]  # make amps a list if not already
        starts = ic['start'] if isinstance(ic['start'], list) else [ic['start']]  # make amps a list if not already
        for amp, start in zip(amps, starts):
            # add stim source
            netParams.stimSourceParams[iclabel+'_'+str(amp)] = {'type': 'IClamp', 'delay': start, 'dur': ic['dur'], 'amp': amp}
            # connect stim source to target
            netParams.stimTargetParams[iclabel+'_'+ic['pop']+'_'+str(amp)] = \
                {'source': iclabel+'_'+str(amp), 'conds': {'pop': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}