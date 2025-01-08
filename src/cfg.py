from netpyne.batchtools import specs

### config ###
cfg = specs.SimConfig()

cfg.preStim = 1800
cfg.postStim = 2000
cfg.duration = cfg.preStim + cfg.postStim
cfg.GoNoGo = 'Go'
cfg.Condition = 'MirrorDecre'+'_'+cfg.GoNoGo
# Membrane time constant of model is actually larger than experiment, thus for longer synapses,
# membrane will decay slower to resting membrane potential, which is a problem
# We compensate this effect by changing the taus to make synapses faster. Original values cfg.tau1 = 10
# cfg.tau2 = 80
cfg.tau1 = 5 #10
cfg.tau2 = 60 #80
cfg.RangeConnectionsCFA = [57, 87] # Average connections from CFA to FoxP2 is 72±15. Not used yet. RELEVANT!
cfg.RangeConnectionsRFA = [66, 144] # Average connections from RFA to FoxP2 is 105±39. Not used yet
cfg.IncreConn = 18
cfg.DecreConn = 51
cfg.NotChangingConn = 4
cfg.numTrials = 100
cfg.synsPerConn = 1
#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.dt = 0.1
cfg.v_init = -80
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321}
cfg.hParams = {'celsius': 37, 'v_init': cfg.v_init}
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
cfg.saveDataInclude = ['simData', 'simConfig']#['simData', 'simConfig', 'netParams', 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/']
cfg.gatherOnlySimData = False
cfg.saveCellSecs = False
cfg.saveCellConns = True

cfg.addIClamp=True
cfg.IAmp = 0  # nA
# current injection params
cfg.IClamp1 = {'pop': 'FoxP2', 'sec': 'soma', 'loc': 0.5, 'dur': cfg.duration, 'amp': cfg.IAmp, 'start': 0}

cfg.addVecStim = True
cfg.AMPANMDAWeightsIncre = 0.004 # 0.004 for 200 pA of EPSC, 0.008 for 400 pA of EPSC
cfg.AMPANMDAWeightsDecre = 0.004
cfg.AMPANMDAWeightsNotChanging = 0.004

cfg.simLabel = 'FoxP2_VecStim_%s_%s_%s/FoxP2' % (cfg.Condition, cfg.IncreConn, cfg.DecreConn)

cfg.somaProb = 0.2
cfg.delay = 2
cfg.ESynMech = 'AMPA'

cfg.addNetStim = True
cfg.NetStimRatePre = 6.7  # From firing rate in Hz to Interval the conversion is Interval[ms] = 1000/Freq[Hz]
cfg.NetStimRatePost = 6.7*0.87  # From firing rate in Hz to Interval the conversion is Interval[ms] = 1000/Freq[Hz]
cfg.NetStimRateDesv = 4.7
cfg.NetStimNoise = 0.71  # Fraction of noise in NetStim (0 = deterministic; 1 = completely random). 1 means that there is no refractory period between NetStims
cfg.NetStimWeight = 0.004
cfg.NetStimNumber = 1e10  # Max number of spikes generated (default = 1e12)
cfg.NetStimDelay = cfg.delay

#####################
transitory = 400
timeRange = [transitory, cfg.duration-100]
cfg.format = 'png'

cfg.analysis['plotTraces'] = {'include': [('FoxP2', i) for i in range(5)], 'timeRange': timeRange,
                              'oneFigPer': 'trace', 'overlay': False, 'figSize': (10, 10),
                              'saveFig': True, 'fileType': cfg.format,
                              'showFig': False}

cfg.analysis['plotRaster'] = {'include': [('FoxP2', i) for i in range(cfg.numTrials)], 'timeRange': timeRange,
                              'orderInverse': False, 'figSize': (5, 5),
                              'saveFig': True, 'fileType': cfg.format,
                              'showFig': False}

cfg.analysis['plotSpikeFreq'] = {'include': ['FoxP2'], 'timeRange': timeRange, 'measure': 'rate', 'binSize': 40,
                                 'saveFig': True, 'fileType': cfg.format,
                                 'showFig': False, 'density': False,
                                 'xlabel': 'Time (ms)', 'marker': 'x'}