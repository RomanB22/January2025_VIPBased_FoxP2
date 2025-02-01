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
from neuron import h

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
cfg, netParams = sim.readCmdLineArgs(simConfigDefault='fI_curve_calibration/cfg.py', netParamsDefault='fI_curve_calibration/netParams.py')

sim.initialize(simConfig = cfg, netParams = netParams)  # create network object and set cfg and net params

sim.pc.timeout(300)                          # set nrn_timeout threshold to X sec (max time allowed without increasing simulation time, t; 0 = turn off)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)


impedance_data = {}

# Create the impedance object
zz = h.Impedance()

def rn(t):
    """Compute and return the DC input resistance at the middle of the soma."""
    zz.loc(0.5)  # Set the reference location for impedance calculations
    zz.compute(0)  # Compute DC input resistance (0 Hz)
    rn_value = zz.input(0.5)  # Get input resistance at the same location (middle of soma)
    # If 't' is already a key in the dictionary, append the value to the list
    if t in impedance_data:
        impedance_data[t].append(rn_value)
    else:
        impedance_data[t] = [rn_value]  # If it's the first time 't' appears, create a list
    return print(f'The impedance value for {t} is ',rn_value,'Ohms')

# Simulation option 1: standard
# sim.runSim()

#Simulation option 2: intervals
sim.runSimWithIntervalFunc(cfg.saveInterval, rn)

# Gather/save data option 1: standard
sim.gatherData()

# Gather/save data option 2: distributed saving across nodes
#sim.saveDataInNodes()
#sim.gatherDataFromFiles()

sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc

import matplotlib.pyplot as plt
import json

def plot_impedance(impedance_data):
    with open("data/"+cfg.simLabel+"Impedance.json", "w") as json_file:
        json.dump(impedance_data, json_file, indent=4)

    """Plot impedance values over time."""
    times = list(impedance_data.keys())
    impedances = list(impedance_data.values())

    plt.figure(figsize=(8, 5))
    plt.plot(times, impedances, marker='o', linestyle='-', color='b', label='Impedance (Ohms)')
    plt.xlabel("Time")
    plt.ylabel("Impedance (Ohms)")
    plt.title("Impedance over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig("data/"+cfg.simLabel+"Impedance")
    

plot_impedance(impedance_data)