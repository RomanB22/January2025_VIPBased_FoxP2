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
tunedParamsOrigOkayApril182025 = {
            "ori1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.033555847038423514,
                    "taus": 211.23700071307496
                },
                "Ra": 155.83389080881165,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 1.0451442563212505,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.007147618107147519,
                    "valf": -11.981651973315863
                },
                "pas": {
                    "e": -62.82994891348203,
                    "g": 4.897617432045613e-05
                }
            },
            "ori2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.04305241587483605,
                    "taus": 211.07999148245977
                },
                "Ra": 294.6369875291328,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.9823946059056765,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.001995905733126572,
                    "valf": -12.004808794030545
                },
                "pas": {
                    "e": -77.3094379486532,
                    "g": 5.6198048184593156e-05
                }
            },
            "rad1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.03617300077643632,
                    "taus": 211.50728710504103
                },
                "Ra": 247.4877878165534,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.7979100709977925,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.0030197298055870815,
                    "valf": -14.292786550831941
                },
                "pas": {
                    "e": -43.18823478422753,
                    "g": 4.489207710979671e-05
                }
            },
            "rad2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.0075547270702817915,
                    "taus": 212.0558493893737
                },
                "Ra": 116.66549376685347,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 1.2054432876541832,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.006676979378995631,
                    "valf": -12.509171736433393
                },
                "pas": {
                    "e": -52.16771712825026,
                    "g": 5.663964256510521e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.02864511425205868,
                    "taus": 213.82290743717624
                },
                "Ra": 161.86087110491243,
                "cancr": {
                    "gcabar": 0.001272339818569152
                },
                "cm": 0.19000290878151518,
                "iCcr": {
                    "gkcbar": 0.002682049431287712
                },
                "kdrcr": {
                    "gkdrbar": 0.0027081909939373934,
                    "valf": -12.927293984218267
                },
                "pas": {
                    "e": -81.53814161804004,
                    "g": 2.7926922393979932e-05
                }
            }
        }

tunedParamsOrigBetterApril182025 = {
            "ori1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.03620051664945352,
                    "taus": 209.6402667869049
                },
                "Ra": 156.48488866793994,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.9862606024212732,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.007620749947248059,
                    "valf": -11.238475569220446
                },
                "pas": {
                    "e": -68.94520281296299,
                    "g": 4.9690008977514214e-05
                }
            },
            "ori2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.04637756634393874,
                    "taus": 195.75000066315047
                },
                "Ra": 149.16544292366643,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.894380975574114,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.001989049667110744,
                    "valf": -11.991581787070174
                },
                "pas": {
                    "e": -82.55328942703039,
                    "g": 5.9458077693878924e-05
                }
            },
            "rad1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.0383372229380183,
                    "taus": 200.03659251492624
                },
                "Ra": 139.1751560040922,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.7800140087280175,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.0027802038807920797,
                    "valf": -15.416421652927266
                },
                "pas": {
                    "e": -39.834587008644164,
                    "g": 4.512702470327495e-05
                }
            },
            "rad2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.007115974529340965,
                    "taus": 213.42669283460768
                },
                "Ra": 141.7078212258808,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 1.207283724387104,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.006604210608652641,
                    "valf": -13.073161566111239
                },
                "pas": {
                    "e": -53.397303942965394,
                    "g": 5.481073970515329e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.029258105672312417,
                    "taus": 208.46441586035667
                },
                "Ra": 135.11537924391862,
                "cancr": {
                    "gcabar": 0.001200673446931951
                },
                "cm": 0.1762111618060807,
                "iCcr": {
                    "gkcbar": 0.002739309869536659
                },
                "kdrcr": {
                    "gkdrbar": 0.002731219341601073,
                    "valf": -11.792996540097391
                },
                "pas": {
                    "e": -74.63132881332893,
                    "g": 2.98701167732318e-05
                }
            }
        }

tunedParams = tunedParamsOrigBetterApril182025

cellRule = netParams.importCellParams(label='FoxP2', conds={'cellType': 'FoxP2', 'cellModel': 'HH_reduced'},
                                      fileName=cfg.hocFile, cellName='FoxP2', importSynMechs = True)

cellRule['secs']['soma']['mechs']['Nafcr']['gnafbar'] = tunedParams['soma']['Nafcr']['gnafbar']
cellRule['secs']['soma']['mechs']['Nafcr']['taus'] = tunedParams['soma']['Nafcr']['taus']
cellRule['secs']['soma']['mechs']['kdrcr']['gkdrbar'] = tunedParams['soma']['kdrcr']['gkdrbar']
cellRule['secs']['soma']['mechs']['kdrcr']['valf'] = tunedParams['soma']['kdrcr']['valf']
cellRule['secs']['soma']['mechs']['IKscr']['gKsbar'] = tunedParams['soma']['IKscr']['gKsbar']
cellRule['secs']['soma']['mechs']['iCcr']['gkcbar'] = tunedParams['soma']['iCcr']['gkcbar']
cellRule['secs']['soma']['mechs']['cancr']['gcabar'] = tunedParams['soma']['cancr']['gcabar']
cellRule['secs']['soma']['mechs']['pas']['e'] = tunedParams['soma']['pas']['e']
cellRule['secs']['soma']['geom']['cm'] = tunedParams['soma']['cm']
cellRule['secs']['soma']['geom']['Ra'] = tunedParams['soma']['Ra']
cellRule['secs']['soma']['mechs']['pas']['g'] = tunedParams['soma']['pas']['g']

for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
    cellRule['secs'][sec]['mechs']['Nafcr']['gnafbar'] = tunedParams[sec]['Nafcr']['gnafbar']
    cellRule['secs'][sec]['mechs']['Nafcr']['taus'] = tunedParams[sec]['Nafcr']['taus']
    cellRule['secs'][sec]['mechs']['kdrcr']['gkdrbar'] = tunedParams[sec]['kdrcr']['gkdrbar']
    cellRule['secs'][sec]['mechs']['kdrcr']['valf'] = tunedParams[sec]['kdrcr']['valf']
    cellRule['secs'][sec]['mechs']['IKscr']['gKsbar'] = tunedParams[sec]['IKscr']['gKsbar']
    cellRule['secs'][sec]['mechs']['iCcr']['gkcbar'] = tunedParams[sec]['iCcr']['gkcbar']
    cellRule['secs'][sec]['mechs']['cancr']['gcabar'] = tunedParams[sec]['cancr']['gcabar']
    cellRule['secs'][sec]['mechs']['pas']['e'] = tunedParams[sec]['pas']['e']
    cellRule['secs'][sec]['geom']['cm'] = tunedParams[sec]['cm']
    cellRule['secs'][sec]['geom']['Ra'] = tunedParams[sec]['Ra']
    cellRule['secs'][sec]['mechs']['pas']['g'] = tunedParams[sec]['pas']['g']

cellRule['secLists']['spiny'] = ['rad1', 'rad2', 'ori1', 'ori2']

if cfg.blockNa=='True':
    for sec in ['soma', 'rad1', 'rad2', 'ori1', 'ori2']:
        cellRule['secs'][sec]['mechs']['Nafcr']['gnafbar'] = 0

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
                try:
                    spkTimes = Results[Condition][trial][cell]['SimSpks'][RandomRealization]
                except:
                    continue
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

def ScaleSpikeTimingAfterMovement(spikeTimes, factorWidth, movementTime):
    spikeTimesTrial = []
    for i in spikeTimes:
        i = np.array(i)
        premov = i[i<=movementTime]
        postmov = i[i>movementTime]
        try:
            diffpost = postmov-postmov[0]
            scaledpostmov = postmov[0] + factorWidth*diffpost
        except:
            scaledpostmov = postmov

        spikeTimesTrial.append(np.ndarray.tolist(np.hstack((premov, scaledpostmov))))

    return spikeTimesTrial

# In order to update the previous value after the cfg.update_cfg()
cfg.IncreConn = cfg.IncDec[0]
cfg.DecreConn = cfg.IncDec[1]

if cfg.addVecStim:
    ####
    # Load the spike trains
    if str(cfg.GoNoGo) == 'Go':
        if cfg.Fitting == 'True':
            if cfg.ConstantArea == 'True':
                with open('cells/SimSpikes/ResultsNewJuly2025_%s_%1.2f_%1.2f_%s_ConstantArea.pkl' % (cfg.GoNoGo, cfg.factorAmp, cfg.factorWidth, cfg.Fitting), 'rb') as results:
                    Results = pickle.load(results)
            else:
                with open('cells/SimSpikes/ResultsNewJuly2025_%s_%1.2f_%1.2f_%s.pkl' % (cfg.GoNoGo, cfg.factorAmp, cfg.factorWidth, cfg.Fitting), 'rb') as results:
                    Results = pickle.load(results)
        else:
            with open('cells/SimSpikes/ResultsNewJuly2025_%s_%1.2f_%1.2f_%s.pkl' % (cfg.GoNoGo, cfg.factorAmp, 1.0, cfg.Fitting), 'rb') as results:
                Results = pickle.load(results)
    elif str(cfg.GoNoGo) == 'NoGo':
        with open('cells/SimSpikes/Results_NoGo.pkl', 'rb') as results:
            Results = pickle.load(results)

    AllNeuronsIncre, AllNeuronsDecre, AllNeuronsNotChanging = BagOfSpikeTimes(Results, Condition=cfg.Condition)

    sampledNeuronsIncre, spikeTimesIncre = SampleSpikeTrains(AllNeuronsIncre, numNeurons=cfg.IncreConn,
                                                             numTrials=cfg.numTrials)

    sampledNeuronsDecre, spikeTimesDecre = SampleSpikeTrains(AllNeuronsDecre, numNeurons=cfg.DecreConn,
                                                             numTrials=cfg.numTrials)

    sampledNeuronsNotChanging, spikeTimesNotChanging = SampleSpikeTrains(AllNeuronsNotChanging,
                                                                         numNeurons=cfg.NotChangingConn,
                                                                         numTrials=cfg.numTrials)

    if cfg.TwoStims == 'True':
        AllNeuronsIncre2, dummy, dummy = BagOfSpikeTimes(Results, Condition=cfg.Condition)
        sampledNeuronsIncre2, spikeTimesIncre2 = SampleSpikeTrains(AllNeuronsIncre2, numNeurons=cfg.IncreConn,
                                                                 numTrials=cfg.numTrials)
        # Second movement is just the part of the inputs after the movement part
        for i in range(len(spikeTimesIncre2)):
            spikeAux = []
            for j in spikeTimesIncre2[i]:
                array = np.array(j, dtype=float)
                postmov = np.ndarray.tolist(array[array>=cfg.preStim])
                spikeAux.append(postmov)
            spikeTimesIncre2[i] = spikeAux

    netParams.popParams['FoxP2'] = {'cellModel': 'HH_reduced', 'cellType': 'FoxP2', 'numCells': cfg.numTrials}

    for Trial in range(cfg.numTrials):
        spikeTimesIncreTrial = spikeTimesIncre[Trial]
        spikeTimesDecreTrial = spikeTimesDecre[Trial]
        spikeTimesNotChangingTrial = spikeTimesNotChanging[Trial]

        if cfg.TwoStims == 'True':
            spikeTimesIncreTrial2 = spikeTimesIncre2[Trial]
            spikeTimesIncreTrial2 = ScaleSpikeTimingAfterMovement(spikeTimesIncreTrial2, factorWidth=cfg.factorWidth,
                                                                 movementTime=cfg.preStim)
        ### Scale postmovement spikes for CSN_inc population (carrier of the movement signal)
        spikeTimesIncreTrial = ScaleSpikeTimingAfterMovement(spikeTimesIncreTrial, factorWidth=cfg.factorWidth, movementTime=cfg.preStim)

        ### Define Populations
        if cfg.IncreConn > 0:
            netParams.popParams[f'Increasing_{Trial}'] = {'cellModel': 'VecStim',
                                                          'numCells': len(spikeTimesIncreTrial),
                                                          'spkTimes': spikeTimesIncreTrial}
            if cfg.TwoStims == 'True':
                netParams.popParams[f'Increasing2_{Trial}'] = {'cellModel': 'VecStim',
                                                              'numCells': len(spikeTimesIncreTrial2),
                                                              'spkTimes': spikeTimesIncreTrial2}
        if cfg.DecreConn > 0:
            netParams.popParams[f'Decreasing_{Trial}'] = {'cellModel': 'VecStim',
                                                          'numCells': len(spikeTimesDecreTrial),
                                                          'spkTimes': spikeTimesDecreTrial}
        if cfg.NotChangingConn>0:
            netParams.popParams[f'NotChanging_{Trial}'] = {'cellModel': 'VecStim',
                                                           'numCells': len(spikeTimesNotChangingTrial),
                                                           'spkTimes': spikeTimesNotChangingTrial}

        Weights = {'Increasing': cfg.AMPANMDAWeightsIncre, 'Decreasing': cfg.AMPANMDAWeightsDecre,
                   'NotChanging': cfg.AMPANMDAWeightsNotChanging, 'Increasing2': cfg.AMPANMDAWeightsIncre,}

        # ------------------------------------------------------------------------------
        # NetStim inputs
        # ------------------------------------------------------------------------------
        if cfg.addNetStim:
            # add stim source
            def poisson_generator(rate, t_start=0.0, t_stop=1000.0, seed=None):
                """
                Returns a SpikeTrain whose spikes are a realization of a Poisson process
                with the given rate (Hz) and stopping time t_stop (milliseconds).

                Note: t_start is always 0.0, thus all realizations are as if
                they spiked at t=0.0, though this spike is not included in the SpikeList.

                Inputs:
                -------
                    rate    - the rate of the discharge (in Hz)
                    t_start - the beginning of the SpikeTrain (in ms)
                    t_stop  - the end of the SpikeTrain (in ms)
                    array   - if True, a np array of sorted spikes is returned,
                                rather than a SpikeTrain object.

                Examples:
                --------
                    >> gen.poisson_generator(50, 0, 1000)
                    >> gen.poisson_generator(20, 5000, 10000, array=True)

                See also:
                --------
                    inh_poisson_generator, inh_gamma_generator, inh_adaptingmarkov_generator
                """

                rng = np.random.RandomState(seed)

                # number = int((t_stop-t_start)/1000.0*2.0*rate)

                # less wasteful than double length method above
                n = (t_stop - t_start) / 1000.0 * rate
                number = np.ceil(n + 3 * np.sqrt(n))
                if number < 100:
                    number = min(5 + np.ceil(2 * n), 100)

                if number > 0:
                    isi = rng.exponential(1.0 / rate, int(number)) * 1000.0
                    if number > 1:
                        spikes = np.add.accumulate(isi)
                    else:
                        spikes = isi
                else:
                    spikes = np.array([])

                spikes += t_start
                i = np.searchsorted(spikes, t_stop)

                extra_spikes = []
                if i == len(spikes):
                    # ISI buf overrun

                    t_last = spikes[-1] + rng.exponential(1.0 / rate, 1)[0] * 1000.0

                    while (t_last < t_stop):
                        extra_spikes.append(t_last)
                        t_last += rng.exponential(1.0 / rate, 1)[0] * 1000.0

                    spikes = np.concatenate((spikes, extra_spikes))

                else:
                    spikes = np.resize(spikes, (i,))

                return spikes
            BackgroundSpikesPre = poisson_generator(cfg.NetStimRatePre, t_start=0.0, t_stop=cfg.preStim, seed=None)
            BackgroundSpikesPost = poisson_generator(cfg.NetStimRatePost, t_start=cfg.preStim, t_stop=cfg.duration, seed=None)

            BackgroundSpikes = np.concatenate((BackgroundSpikesPre, BackgroundSpikesPost))

            netParams.popParams[f'ExtraInputs_{Trial}'] = {'cellModel': 'VecStim',
                                              'numCells': 1,
                                              'spkTimes': BackgroundSpikes.tolist()}
            Weights['ExtraInputs'] = cfg.NetStimWeight

    ####
    # Connect them
    PT5Bpops = [i for i in netParams.popParams.keys() if i != 'FoxP2']

    for InputPops in PT5Bpops:
        delay = cfg.delay
        if InputPops.split('_')[0]=='Increasing2': delay += cfg.SecondStimDelay

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
            'delay': delay,
            'loc': 0.5,
            'synMech': cfg.ESynMech}

        netParams.connParams[connection + '_dend'] = {
            'preConds': {'popLabel': InputPops},
            'postConds': {'popLabel': 'FoxP2'},
            'weight': Weights[InputPops.split('_')[0]],
            'synsPerConn': cfg.synsPerConn,
            'sec': secList,
            'connList': [[i, int(InputPops.split('_')[1])] for i in preSynDend],
            'delay': delay,
            'loc': 'uniform(0,0.8)',
            'synMech': cfg.ESynMech}
else:
    netParams.popParams['FoxP2'] = {'cellModel': 'HH_reduced', 'cellType': 'FoxP2', 'numCells': 1}
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