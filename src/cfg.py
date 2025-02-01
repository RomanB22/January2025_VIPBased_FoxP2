from netpyne.batchtools import specs

### config ###
cfg = specs.SimConfig()

cfg.preStim = 1800
cfg.postStim = 1800
cfg.duration = cfg.preStim + cfg.postStim
cfg.GoNoGo = 'Go'
cfg.Condition = 'InVivo'+'_'+cfg.GoNoGo
# Membrane time constant of model is actually larger than experiment, thus for longer synapses,
# membrane will decay slower to resting membrane potential, which is a problem
# We compensate this effect by changing the taus to make synapses faster.
cfg.tau1 = 3
cfg.tau2 = 10
cfg.RangeConnectionsCFA = [57, 87] # Average connections from CFA to FoxP2 is 72±15. Not used yet. RELEVANT!
cfg.RangeConnectionsRFA = [66, 144] # Average connections from RFA to FoxP2 is 105±39. Not used yet
cfg.IncreConn = 2
cfg.DecreConn = 5
cfg.NotChangingConn = 0
cfg.numTrials = 300
cfg.synsPerConn = 1
#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.dt = 0.1
cfg.v_init = -86
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321}
cfg.hParams = {'celsius': 34, 'v_init': cfg.v_init}
cfg.verbose = 0
cfg.createNEURONObj = True
cfg.createPyStruct = True
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 1.0
cfg.includeParamsLabel = True
cfg.printPopAvgRates = True
cfg.checkErrors = True
cfg.connRandomSecFromList = False
cfg.depolBlockModel = 'False'
cfg.hocFile = 'cells/FoxP2_Jan2025.hoc'
cfg.saveInterval = 50
#------------------------------------------------------------------------------
# Recording
#------------------------------------------------------------------------------
# record from all cells
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}
cfg.recordSpikesGids = ['all']
cfg.recordStim = True
cfg.recordTime = True
cfg.recordStep = 0.1
cfg.recordLFP = False #[[10, y, 90] for y in range(450, 1250, 100)]
cfg.saveLFPCells = False

#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.saveFolder = 'data/'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/']
cfg.gatherOnlySimData = False
cfg.saveCellSecs = False
cfg.saveCellConns = True

cfg.addIClamp=False
cfg.IAmp = 0  # nA
# current injection params
cfg.IClamp1 = {'pop': 'FoxP2', 'sec': 'soma', 'loc': 0.5, 'dur': cfg.duration, 'amp': cfg.IAmp, 'start': 0}

cfg.addVecStim = True
cfg.AMPAWeight = 0.004 # 0.004 for 200 pA of EPSC. It generates around 20 mV of EPSP
cfg.AMPANMDAWeightsIncre = cfg.AMPAWeight
cfg.AMPANMDAWeightsDecre = cfg.AMPAWeight
cfg.AMPANMDAWeightsNotChanging = cfg.AMPAWeight
 # 0.004 for 200 pA of EPSC driven by a NetStim in soma, 0.008 for 400 pA of EPSC
# Since Rin in the model is twice as large than experiment, we use half of the weights,
# to compensate that effect on the membrane potential

cfg.simLabel = 'FoxP2_VecStim_%s_%s_%s_Depol%s/FoxP2' % (cfg.Condition, cfg.IncreConn, cfg.DecreConn, cfg.depolBlockModel)

cfg.somaProb = 0.2
cfg.delay = 3.8
cfg.ESynMech = 'AMPA'

cfg.addNetStim = True
cfg.NoiseMultiplier = 1 # 1e-10 (or whatever small number larger than zero) or 1 to use the In-vivo background noise
cfg.NetStimRatePre = max(cfg.NoiseMultiplier, 1e-10)*6.7  # From firing rate in Hz to Interval the conversion is Interval[ms] = 1000/Freq[Hz]
cfg.NetStimRateProportion = 0.87
cfg.NetStimRatePost = max(cfg.NoiseMultiplier, 1e-10)*6.7*cfg.NetStimRateProportion  # From firing rate in Hz to Interval the conversion is Interval[ms] = 1000/Freq[Hz]
cfg.NetStimRateDesv = 4.7
cfg.NetStimNoise = 0.71  # Fraction of noise in NetStim (0 = deterministic; 1 = completely random). 1 means that there is no refractory period between NetStims
cfg.NetStimWeight = cfg.AMPAWeight
cfg.NetStimNumber = 1e10  # Max number of spikes generated (default = 1e12)
cfg.NetStimDelay = cfg.delay

#####################
transitory = 800
timeRange = [transitory, cfg.duration-100]
cfg.format = 'png'

cfg.analysis['plotTraces'] = {'include': [('FoxP2', i) for i in range(5)], 'timeRange': timeRange,
                              'oneFigPer': 'trace', 'overlay': False, 'figSize': (10, 10),
                              'saveFig': True, 
                              'showFig': False}

cfg.analysis['plotRaster'] = {'include': [('FoxP2', i) for i in range(cfg.numTrials)], 'timeRange': timeRange,
                              'orderInverse': False, 'figSize': (5, 5),
                              'saveFig': True, 
                              'showFig': False}

cfg.analysis['plotSpikeFreq'] = {'include': ['FoxP2'], 'timeRange': timeRange, 'measure': 'rate', 'binSize': 40,
                                 'saveFig': True, 
                                 'showFig': False, 'density': False,
                                 'xlabel': 'Time (ms)', 'marker': 'x'}