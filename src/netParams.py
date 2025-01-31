from netpyne.batchtools import specs
from src.cfg import cfg
import pickle
import random
import numpy as np

cfg.update_cfg()
### params ###
# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters
netParams.defaultThreshold = -10
netParams.defineCellShapes = False       # sets 3d geometry aligned along the y-axis
netParams.version = 1
###############################################################################
## Cell types
###############################################################################
tunedParamsNoDepol = {
            "ori1": {
                "Nafcr": {
                    "gnafbar": 0.029965488148624903
                },
                "Ra": 94.74718339461782,
                "cm": 1.5176378820670497,
                "kdrcr": {
                    "gkdrbar": 0.006694501704851497
                },
                "pas": {
                    "e": -54.2289806909487,
                    "g": 5.257002446478203e-06
                }
            },
            "ori2": {
                "Nafcr": {
                    "gnafbar": 0.038223933270564815
                },
                "Ra": 132.73532224173897,
                "cm": 2.15072603453916,
                "kdrcr": {
                    "gkdrbar": 0.010723434637928886
                },
                "pas": {
                    "e": -63.62680070683853,
                    "g": 1.4278457683822263e-05
                }
            },
            "rad1": {
                "Nafcr": {
                    "gnafbar": 0.09609176242393565
                },
                "Ra": 111.19659944041622,
                "cm": 3.133558790101724,
                "kdrcr": {
                    "gkdrbar": 0.016011530234952602
                },
                "pas": {
                    "e": -72.61032815286347,
                    "g": 9.211499195069896e-05
                }
            },
            "rad2": {
                "Nafcr": {
                    "gnafbar": 0.12820290017177124
                },
                "Ra": 111.76668505024826,
                "cm": 2.064580707959245,
                "kdrcr": {
                    "gkdrbar": 0.011384794197403585
                },
                "pas": {
                    "e": -69.99699610107999,
                    "g": 6.254791049107461e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.004999550461485062
                },
                "Nafcr": {
                    "gnafbar": 0.00792241108927046
                },
                "Ra": 115.43187325932695,
                "cancr": {
                    "gcabar": 0.009041149398789038
                },
                "cm": 2.0750330942221358,
                "iCcr": {
                    "gkcbar": 0.00010672629071301523
                },
                "kdrcr": {
                    "gkdrbar": 0.017264335382227255
                },
                "pas": {
                    "e": -66.36873979773242,
                    "g": 4.332376755670617e-06
                }
            }
        }
tunedParamsDepol = {
            "ori1": {
                "Nafcr": {
                    "gnafbar": 0.041000776990370955
                },
                "Ra": 106.06500632460752,
                "cm": 1.906196295433552,
                "kdrcr": {
                    "gkdrbar": 0.007320736778279362
                },
                "pas": {
                    "e": -65.14774283511437,
                    "g": 5.218995591233591e-06
                }
            },
            "ori2": {
                "Nafcr": {
                    "gnafbar": 0.02431242420897496
                },
                "Ra": 141.65175546317616,
                "cm": 2.5636753366991925,
                "kdrcr": {
                    "gkdrbar": 0.009650373554419302
                },
                "pas": {
                    "e": -47.666777104659324,
                    "g": 1.1238688624912248e-05
                }
            },
            "rad1": {
                "Nafcr": {
                    "gnafbar": 0.11208489961757948
                },
                "Ra": 118.45657608813895,
                "cm": 2.639102978751162,
                "kdrcr": {
                    "gkdrbar": 0.014750759942096462
                },
                "pas": {
                    "e": -84.05610526920424,
                    "g": 0.00010460312501858911
                }
            },
            "rad2": {
                "Nafcr": {
                    "gnafbar": 0.11932892724494704
                },
                "Ra": 111.97011485002753,
                "cm": 1.7829463724726895,
                "kdrcr": {
                    "gkdrbar": 0.011774900951697054
                },
                "pas": {
                    "e": -58.492141375012764,
                    "g": 7.0750758261592e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.006764783988271673
                },
                "Nafcr": {
                    "gnafbar": 0.007049291668535117
                },
                "Ra": 84.8227052914339,
                "cancr": {
                    "gcabar": 0.007741530629330753
                },
                "cm": 1.8675985494287146,
                "iCcr": {
                    "gkcbar": 9.691139847500207e-05
                },
                "kdrcr": {
                    "gkdrbar": 0.010985836518386883
                },
                "pas": {
                    "e": -51.29333525759825,
                    "g": 5.274328478094304e-06
                }
            }
        }

if cfg.depolBlockModel=='True':
    tunedParams=tunedParamsDepol
    valf = -29
    print("Depol block model")
else:
    tunedParams=tunedParamsNoDepol
    valf = -13
    print("No depol block model")

cellRule = netParams.importCellParams(label='FoxP2', conds={'cellType': 'FoxP2', 'cellModel': 'HH_reduced'},
                                      fileName=cfg.hocFile, cellName='FoxP2', importSynMechs = True)


cellRule['secs']['soma']['mechs']['Nafcr']['gnafbar'] = tunedParams['soma']['Nafcr']['gnafbar']
cellRule['secs']['soma']['mechs']['kdrcr']['gkdrbar'] = tunedParams['soma']['kdrcr']['gkdrbar']
cellRule['secs']['soma']['mechs']['kdrcr']['valf'] = valf
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
    cellRule['secs'][sec]['mechs']['kdrcr']['valf'] = valf
    cellRule['secs'][sec]['mechs']['pas']['e'] = tunedParams[sec]['pas']['e']
    cellRule['secs'][sec]['geom']['cm'] = tunedParams[sec]['cm']
    cellRule['secs'][sec]['geom']['Ra'] = tunedParams[sec]['Ra']
    cellRule['secs'][sec]['mechs']['pas']['g'] = tunedParams[sec]['pas']['g']

cellRule['secLists']['spiny'] = ['rad1', 'rad2', 'ori1', 'ori2']

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
    # import json
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
        if cfg.IncreConn > 0:
            netParams.popParams[f'Increasing_{Trial}'] = {'cellModel': 'VecStim',
                                                          'numCells': len(spikeTimesIncreTrial),
                                                          'spkTimes': spikeTimesIncreTrial}
        if cfg.DecreConn > 0:
            netParams.popParams[f'Decreasing_{Trial}'] = {'cellModel': 'VecStim',
                                                          'numCells': len(spikeTimesDecreTrial),
                                                          'spkTimes': spikeTimesDecreTrial}
        if cfg.NotChangingConn>0:
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