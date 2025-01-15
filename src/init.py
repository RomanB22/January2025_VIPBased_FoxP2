from netpyne.batchtools import specs, comm
from netpyne import sim
from src.netParams import netParams, cfg
import json
comm.initialize()

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)
print('completed simulation...')

# Next part is just to avoid errors from the ray package, not necessary
if comm.is_host():
    inputs = specs.get_mappings()
    results = {}
    results['loss'] = 10000 # A dummy value
    out_json = json.dumps({**inputs, **results})
    comm.send(out_json)
    comm.close()