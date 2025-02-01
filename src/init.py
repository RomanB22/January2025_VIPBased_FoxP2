from netpyne.batchtools import specs, comm
from netpyne import sim
from src.netParams import netParams, cfg
import json
comm.initialize()

# sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)


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
cfg, netParams = sim.readCmdLineArgs(simConfigDefault='src/cfg.py', netParamsDefault='src/netParams.py')

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
    for cell in sim.net.cells: 
        if not str(cell).startswith('compartCell'):
            continue  # Skip cells that are not foxp2
        #print('aaaaaaaaaaaaaaaaaa',cell.secs)
        #print(cell)
        zz.loc(0.5, sec=cell.secs['soma']['hObj'] )  # Set the reference location for impedance calculations
        zz.compute(0)  # Compute DC input resistance (0 Hz)
        rn_value = zz.input(0.5,sec=cell.secs['soma']['hObj'] )  # Get input resistance at the same location (middle of soma)
        
        if t in impedance_data:
            impedance_data[t].append(rn_value)
        else:
            impedance_data[t] = [rn_value]  # If it's the first time 't' appears, create a list
        print(f'The impedance value for {t} is ',rn_value,'Ohms')
    

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
import numpy as np

def plot_impedance(impedance_data):
    # Save the impedance data to a JSON file
    with open("data/" + cfg.simLabel + "Impedance.json", "w") as json_file:
        json.dump(impedance_data, json_file, indent=4)
    
    """Plot impedance values over time."""
    times = np.array(list(map(float, impedance_data.keys())))  # Convert times to float
    impedances = list(impedance_data.values())  # List of lists of impedance values

    # Number of curves (each curve corresponds to the same index across all times)
    num_curves = len(impedances[0])

    # Plot all curves
    plt.figure(figsize=(20, 10))
    for i in range(num_curves):
        curve = [impedances[j][i] for j in range(len(impedances))]  # Extract the i-th curve
        plt.plot(times, curve, marker='o', linestyle='-', alpha=0.5, label=f'Curve {i+1}')

    # Calculate and plot the average curve
    avg_curve = np.mean(impedances, axis=1)  # Compute the average at each time step
    plt.plot(times, avg_curve, marker='o', linestyle='-', color='k', linewidth=2, label='Average')

    # Add labels, title, and legend
    plt.xlabel("Time")
    plt.ylabel("Impedance (Ohms)")
    plt.title("Impedance over Time")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()
    plt.savefig("data/" + cfg.simLabel + "Impedance.png")

# Example usage (assuming impedance_data is already populated):
plot_impedance(impedance_data)

print('completed simulation...')

# Next part is just to avoid errors from the ray package, not necessary
if comm.is_host():
    inputs = specs.get_mappings()
    results = {}
    results['loss'] = 10000 # A dummy value
    out_json = json.dumps({**inputs, **results})
    comm.send(out_json)
    comm.close()

