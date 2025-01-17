"""
cfg.py

Simulation configuration for M1 model (using NetPyNE)
"""

from netpyne import specs
import pickle
import numpy as np

cfg = specs.SimConfig()

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 2000
cfg.dt = 0.1
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321}
cfg.hParams = {'celsius': 23, 'v_init': -80}
cfg.verbose = False
cfg.createNEURONObj = True
cfg.createPyStruct = True
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.1
cfg.includeParamsLabel = True
cfg.printPopAvgRates = True
cfg.checkErrors = True
cfg.connRandomSecFromList = False
cfg.depolBlockModel = False
cfg.hocFile = 'cells/FoxP2_Jan2025.hoc'
#------------------------------------------------------------------------------
# Recording
#------------------------------------------------------------------------------
cfg.recordSpikesGids = ['all']
cfg.recordStim = True
cfg.recordTime = True
cfg.recordStep = 0.1
cfg.recordLFP = False #[[10, y, 90] for y in range(450, 1250, 100)]
cfg.saveLFPCells = False
cfg.ESynMech = 'AMPA'
cfg.delay = 2
cfg.NetStimWeight = 0.004 # 0.004 for 200 pA of EPSC. It generates around 20 mV of EPSP
cfg.NetStimDelay = cfg.delay
cfg.synsPerConn = 1
# Membrane time constant of model is actually larger than experiment, thus for longer synapses,
# membrane will decay slower to resting membrane potential, which is a problem
# We compensate this effect by changing the taus to make synapses faster. Original values cfg.tau1 = 10
# cfg.tau2 = 80
cfg.tau1 = 5 #10
cfg.tau2 = 60 #80

cfg.InputSection = 'soma' # soma, rad1, rad2, ori1, ori2

# record from all cells
cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'},
                    'I_syn': {'sec': cfg.InputSection, 'loc': 0.5, 'synMech': cfg.ESynMech, 'var': 'i'}}
#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.saveFolder = 'data/'
cfg.simLabel = 'AMPA_SingleInput_Depol%s/FoxP2' % cfg.depolBlockModel
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig'] #['simData', 'simConfig', 'netParams', 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/']
cfg.gatherOnlySimData = False
cfg.saveCellSecs = False
cfg.saveCellConns = True

#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------
cfg.addNetStim = True

cfg.format = 'png'

timeRange = [cfg.duration/2-50, cfg.duration/2+800]
cfg.analysis['plotTraces'] = {'include': ['FoxP2'], 'timeRange': timeRange, 'oneFigPer': 'cell',
                              'figSize': (10, 4), 'saveFig': True, 'showFig': False, 'fileType': cfg.format}

#------------------------------------------------------------------------------
# Parameters
#------------------------------------------------------------------------------
# example of how to set params; but set from batch.py
cfg.tune = specs.Dict()