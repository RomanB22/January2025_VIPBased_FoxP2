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
with open('cells/AverageProperties.pkl', 'rb') as f:
    average_props = pickle.load(f)

timeBetweenCurrentSteps = 1250

transitoryTime = 32
steps = 1
end=15
dur = 432
amps = average_props['f-I Curve'][0][0][::steps]
targetRates = average_props['f-I Curve'][0][1][::steps]

amps = [10 / 1000. * i for i in range(61)]
targetRates = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.298850575, 6.896551724, 9.195402299,
               11.49425287, 13.79310345, 16.09195402, 16.09195402, 18.3908046, 20.68965517, 22.98850575,
               22.98850575, 25.28735632, 27.5862069, 27.5862069, 27.5862069, 29.88505747, 32.18390805, 32.18390805,
               34.48275862, 36.7816092, 36.7816092, 39.08045977, 39.08045977, 39.08045977, 41.37931034, 41.37931034,
               43.67816092, 43.67816092, 45.97701149, 45.97701149, 45.97701149, 48.27586207, 48.27586207,
               50.57471264, 50.57471264, 50.57471264, 52.87356322, 52.87356322, 52.87356322, 52.87356322]

cfg.depolBlockModel = False

amps = amps[::steps]
targetRates = targetRates[::steps]
cfg.simLabel = 'FoxP2_fI_Depol%s/FoxP2' % cfg.depolBlockModel
# For single step simulation uncomment following lines
stepNumber = 21 # each step corresponds to 10 pA increase
amps = [10 / 1000. * stepNumber]
targetRates = [0]
cfg.simLabel = 'FoxP2_fI_Depol%s_%s/FoxP2' % (str(amps), cfg.depolBlockModel)
transitoryTime=132

times = list(np.arange(transitoryTime, timeBetweenCurrentSteps * len(amps), timeBetweenCurrentSteps))  # start times

#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = timeBetweenCurrentSteps * len(amps)
cfg.dt = 0.1
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321}
cfg.hParams = {'celsius': 23, 'v_init': -86}
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
cfg.hocFile = 'cells/FoxP2_Jan2025.hoc'
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
cfg.saveDataInclude = ['simData', 'simConfig'] #['simData', 'simConfig', 'netParams', 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/']
cfg.gatherOnlySimData = False
cfg.saveCellSecs = False
cfg.saveCellConns = True

#------------------------------------------------------------------------------
# Cells
#------------------------------------------------------------------------------
cfg.addIClamp = True

#------------------------------------------------------------------------------
# IClamp stimulus
#------------------------------------------------------------------------------
# current injection params
cfg.IClamp1 = {'pop': 'FoxP2', 'sec': 'soma', 'loc': 0.5, 'dur': dur, 'amp': amps, 'start': times}
cfg.IClamp2 = {'pop': 'FoxP2', 'sec': 'soma', 'loc': 0.5, 'dur': cfg.duration, 'amp': -0.07, 'start': 0}

cfg.format = 'eps'

cfg.analysis['plotfI'] = {'amps': amps, 'times': times, 'dur': dur, 'target': {'rates': targetRates}, 'saveFig': True,
                          'showFig': False, 'calculateFeatures': '', 'fileType': cfg.format}
timeRange = [min(transitoryTime,100), cfg.duration]
cfg.analysis['plotTraces'] = {'include': ['FoxP2'], 'timeRange': timeRange, 'oneFigPer': 'cell',
                              'figSize': (10, 4), 'saveFig': True, 'showFig': False, 'fileType': cfg.format}

#------------------------------------------------------------------------------
# Parameters
#------------------------------------------------------------------------------
# example of how to set params; but set from batch.py
cfg.tune = specs.Dict()