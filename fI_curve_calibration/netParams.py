
"""
netParams.py

High-level specifications for M1 network model using NetPyNE
"""
import os
from netpyne import specs
import pickle, json
import random
import numpy as np

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

netParams.version = 1

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Specification of cell rules not previously loaded
# Includes importing from hoc template or python class, and setting additional params

#------------------------------------------------------------------------------
## PV cell params (3-comp)
#######
# vip-ngf
tunedParamsNoDepol = {
    "ori1": {
        "Nafcr": {
            "gnafbar": 0.0329560444979248
        },
        "Ra": 101.31773619425941,
        "cm": 1.3956569521774433,
        "kdrcr": {
            "gkdrbar": 0.00673548685801663
        },
        "pas": {
            "e": -54.156581525079,
            "g": 5.597266724018472e-06
        }
    },
    "ori2": {
        "Nafcr": {
            "gnafbar": 0.03001174122902476
        },
        "Ra": 126.37477623801631,
        "cm": 2.255656916826277,
        "kdrcr": {
            "gkdrbar": 0.011313713848850666
        },
        "pas": {
            "e": -58.61827939019876,
            "g": 1.3667505345815849e-05
        }
    },
    "rad1": {
        "Nafcr": {
            "gnafbar": 0.10673817803187446
        },
        "Ra": 109.04301401188185,
        "cm": 2.86004280843973,
        "kdrcr": {
            "gkdrbar": 0.013339593274649331
        },
        "pas": {
            "e": -69.94639485920993,
            "g": 9.145445600433023e-05
        }
    },
    "rad2": {
        "Nafcr": {
            "gnafbar": 0.13249929894497717
        },
        "Ra": 105.33290861536801,
        "cm": 1.9340649628033502,
        "kdrcr": {
            "gkdrbar": 0.012867523661924226
        },
        "pas": {
            "e": -69.1936245704239,
            "g": 5.85743110096051e-05
        }
    },
    "soma": {
        "IKscr": {
            "gKsbar": 0.006401436427663786
        },
        "Nafcr": {
            "gnafbar": 0.007063650832394169
        },
        "Ra": 116.63071421583007,
        "cancr": {
            "gcabar": 0.009100552306156038
        },
        "cm": 1.8914506365455446,
        "iCcr": {
            "gkcbar": 0.00010249482863430837
        },
        "kdrcr": {
            "gkdrbar": 0.015069214137235411
        },
        "pas": {
            "e": -68.58434697800882,
            "g": 4.7411099882163505e-06
        }
    }
}

tunedParamsDepol = {
    "ori1": {
        "Nafcr": {
            "gnafbar": 0.04082054365113535
        },
        "Ra": 112.71219260317795,
        "cm": 1.7386428700050718,
        "kdrcr": {
            "gkdrbar": 0.00795423100785642
        },
        "pas": {
            "e": -62.37229768558754,
            "g": 4.798599296528991e-06
        }
    },
    "ori2": {
        "Nafcr": {
            "gnafbar": 0.025482710904591584
        },
        "Ra": 134.49107256418512,
        "cm": 2.5234892981051105,
        "kdrcr": {
            "gkdrbar": 0.009008968739102362
        },
        "pas": {
            "e": -43.89233403429573,
            "g": 1.1620321558477796e-05
        }
    },
    "rad1": {
        "Nafcr": {
            "gnafbar": 0.11257336429562881
        },
        "Ra": 108.58316821600586,
        "cm": 2.7101073300878955,
        "kdrcr": {
            "gkdrbar": 0.01347170651215512
        },
        "pas": {
            "e": -78.27355053698867,
            "g": 9.954710083881613e-05
        }
    },
    "rad2": {
        "Nafcr": {
            "gnafbar": 0.10999874642906309
        },
        "Ra": 102.72694229979082,
        "cm": 1.8347836187385222,
        "kdrcr": {
            "gkdrbar": 0.010863187066404151
        },
        "pas": {
            "e": -64.03154656423675,
            "g": 6.790708995371536e-05
        }
    },
    "soma": {
        "IKscr": {
            "gKsbar": 0.007200984292049982
        },
        "Nafcr": {
            "gnafbar": 0.007048106046995259
        },
        "Ra": 83.22022299421958,
        "cancr": {
            "gcabar": 0.007336735493465247
        },
        "cm": 1.8665330834930678,
        "iCcr": {
            "gkcbar": 9.857697126917098e-05
        },
        "kdrcr": {
            "gkdrbar": 0.011213668755840124
        },
        "pas": {
            "e": -55.01023056726649,
            "g": 4.96316748340829e-06
        }
    }
}

if cfg.depolBlockModel:
    tunedParams=tunedParamsDepol
    valf = -29
else:
    tunedParams=tunedParamsNoDepol
    valf = -13

cellRule = netParams.importCellParams(label='FoxP2', conds={'cellType': 'FoxP2', 'cellModel': 'HH_reduced'},
                                      fileName=cfg.hocFile, cellName='FoxP2', importSynMechs = True)


cellRule['secs']['soma']['mechs']['Nafcr']['gnafbar'] = tunedParams['soma']['Nafcr']['gnafbar']
cellRule['secs']['soma']['mechs']['kdrcr']['gkdrbar'] = tunedParams['soma']['kdrcr']['gkdrbar']
cellRule['secs']['soma']['mechs']['kdrcr']['valf'] = valf
cellRule['secs']['soma']['mechs']['IKscr']['gKsbar'] = tunedParams['soma']['IKscr']['gKsbar']
cellRule['secs']['soma']['mechs']['iCcr']['gkcbar'] = tunedParams['soma']['iCcr']['gkcbar']
cellRule['secs']['soma']['mechs']['cancr']['gcabar'] = tunedParams['soma']['cancr']['gcabar']
# cellRule['secs']['soma']['mechs']['pas']['e'] = tunedParams['soma']['pas']['e']
# cellRule['secs']['soma']['geom']['cm'] = tunedParams['soma']['cm']
cellRule['secs']['soma']['geom']['Ra'] = tunedParams['soma']['Ra']
# cellRule['secs']['soma']['mechs']['pas']['g'] = tunedParams['soma']['pas']['g']

for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
    cellRule['secs'][sec]['mechs']['Nafcr']['gnafbar'] = tunedParams[sec]['Nafcr']['gnafbar']
    cellRule['secs'][sec]['mechs']['kdrcr']['gkdrbar'] = tunedParams[sec]['kdrcr']['gkdrbar']
    cellRule['secs'][sec]['mechs']['kdrcr']['valf'] = valf
    # cellRule['secs'][sec]['mechs']['pas']['e'] = tunedParams[sec]['pas']['e']
    # cellRule['secs'][sec]['geom']['cm'] = tunedParams[sec]['cm']
    cellRule['secs'][sec]['geom']['Ra'] = tunedParams[sec]['Ra']
    # cellRule['secs'][sec]['mechs']['pas']['g'] = tunedParams[sec]['pas']['g']

cellRule['secLists']['spiny'] = ['rad1', 'rad2', 'ori1', 'ori2']

# with open('cellJSON.json', 'w') as f:
#     json.dump(cellRule, f)

# For tuning the model and calibrate it
for sec, secDict in netParams.cellParams['FoxP2']['secs'].items():
    if sec in cfg.tune:
        # vinit
        if 'vinit' in cfg.tune[sec]:
            secDict['vinit'] = cfg.tune[sec]['vinit']

        # mechs
        for mech in secDict['mechs']:
            if mech in cfg.tune[sec]:
                for param in secDict['mechs'][mech]:
                    if param in cfg.tune[sec][mech]:
                        secDict['mechs'][mech][param] = cfg.tune[sec][mech][param]

        # geom
        for geomParam in secDict['geom']:
            if geomParam in cfg.tune[sec]:
                secDict['geom'][geomParam] = cfg.tune[sec][geomParam]

# ------------------------------------------------------------------------------
# Create population
# ------------------------------------------------------------------------------
netParams.popParams['FoxP2'] = {'cellModel': 'HH_reduced', 'cellType': 'FoxP2', 'numCells': 1}
#------------------------------------------------------------------------------
# Current inputs (IClamp)
#------------------------------------------------------------------------------
if cfg.addIClamp:
     for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params
        amps = ic['amp'] if isinstance(ic['amp'], list) else [ic['amp']]  # make amps a list if not already
        starts = ic['start'] if isinstance(ic['start'], list) else [ic['start']]  # make amps a list if not already
        for amp, start in zip(amps, starts):
            # add stim source
            netParams.stimSourceParams[iclabel+'_'+str(amp)] = {'type': 'IClamp', 'delay': start, 'dur': ic['dur'], 'amp': amp}
            # connect stim source to target
            netParams.stimTargetParams[iclabel+'_'+ic['pop']+'_'+str(amp)] = \
                {'source': iclabel+'_'+str(amp), 'conds': {'pop': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}
