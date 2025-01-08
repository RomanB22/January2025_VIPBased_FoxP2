"""
init.py

Starting script to run NetPyNE-based PT model.

Usage:
    python sim/init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi sim/init.py
"""

#import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers

from netpyne import sim

#cfg, netParams = sim.loadFromIndexFile('index.npjson')
"""
init.py

Starting script to run NetPyNE-based M1 model.

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: salvadordura@gmail.com
"""

import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim

# -----------------------------------------------------------
# Main code
# Option to run one example
#cfg, netParams = sim.loadFromIndexFile('index.npjson')
# Option necessary for batch to work
cfg, netParams = sim.readCmdLineArgs(simConfigDefault='AMPA_weight_calibration/cfg.py', netParamsDefault='AMPA_weight_calibration/netParams.py')

sim.initialize(simConfig = cfg, netParams = netParams)  # create network object and set cfg and net params

sim.pc.timeout(300)                          # set nrn_timeout threshold to X sec (max time allowed without increasing simulation time, t; 0 = turn off)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)

# Simulation option 1: standard
sim.runSim()

# Gather/save data option 1: standard
sim.gatherData()

# Gather/save data option 2: distributed saving across nodes
#sim.saveDataInNodes()
#sim.gatherDataFromFiles()

sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc