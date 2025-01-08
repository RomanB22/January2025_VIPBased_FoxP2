from netpyne.batchtools import specs, comm
from netpyne import sim
from src.netParams import netParams, cfg

comm.initialize()

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)
print('completed simulation...')