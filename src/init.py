from netpyne.batchtools import specs, comm
from netpyne import sim
from src.netParams import netParams, cfg
import json
def rn(t, impedanceData, movementTime=1800):
    """Compute and return the DC input resistance at the middle of the soma."""
    from neuron import h
    from netpyne import sim

    # Create the impedance object
    zz = h.Impedance()

    for cell in sim.net.cells:
        if not str(cell).startswith('compartCell'): # Skip cells that are not FoxP2
            continue
        zz.loc(0.5, sec=cell.secs['soma']['hObj'])  # Set the reference location for impedance calculations
        zz.compute(0)  # Compute DC input resistance (0 Hz)
        rn_value = zz.input(0.5, sec=cell.secs['soma']['hObj'])  # Get input resistance at the same location (middle of soma)

        time = round(t, 1)
        if time in impedanceData:
            impedanceData[time].append(rn_value)
        else:
            impedanceData[time] = [rn_value]  # If it's the first time 't' appears, create a list
        # print(f'The impedance value for {t} is ', rn_value, 'MOhms')
    sim.simData.Impedance = impedanceData

comm.initialize()


# -----------------------------------------------------------
# Main code
# Option to run one example
#cfg, netParams = sim.loadFromIndexFile('index.npjson')
sim.initialize(simConfig = cfg, netParams = netParams)  # create network object and set cfg and net params

sim.pc.timeout(300)                          # set nrn_timeout threshold to X sec (max time allowed without increasing simulation time, t; 0 = turn off)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)

# Simulation option 1: standard
# sim.runSim()
#Simulation option 2: intervals
impedanceData = {}
sim.runSimWithIntervalFunc(cfg.saveInterval, rn, funcArgs={'impedanceData': impedanceData})

# Gather/save data option 1: standard
sim.gatherData()

# Gather/save data option 2: distributed saving across nodes
#sim.saveDataInNodes()
#sim.gatherDataFromFiles()

sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
sim.analysis.plotData()         			# plot spike raster etc

print('completed simulation...')

# Next part is just to avoid errors from the ray package, not necessary
if comm.is_host():
    inputs = specs.get_mappings()
    results = {}
    results['loss'] = 10000 # A dummy value
    out_json = json.dumps({**inputs, **results})
    comm.send(out_json)
    comm.close()