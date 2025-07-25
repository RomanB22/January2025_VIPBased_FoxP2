
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
netParams.defaultThreshold = cfg.spikeThreshold

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Specification of cell rules not previously loaded
# Includes importing from hoc template or python class, and setting additional params

#------------------------------------------------------------------------------
## PV cell params (3-comp)
#######

tunedParamsOrigOkayApril182025 = {
            "ori1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.033555847038423514,
                    "taus": 211.23700071307496
                },
                "Ra": 155.83389080881165,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 1.0451442563212505,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.007147618107147519,
                    "valf": -11.981651973315863
                },
                "pas": {
                    "e": -62.82994891348203,
                    "g": 4.897617432045613e-05
                }
            },
            "ori2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.04305241587483605,
                    "taus": 211.07999148245977
                },
                "Ra": 294.6369875291328,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.9823946059056765,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.001995905733126572,
                    "valf": -12.004808794030545
                },
                "pas": {
                    "e": -77.3094379486532,
                    "g": 5.6198048184593156e-05
                }
            },
            "rad1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.03617300077643632,
                    "taus": 211.50728710504103
                },
                "Ra": 247.4877878165534,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.7979100709977925,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.0030197298055870815,
                    "valf": -14.292786550831941
                },
                "pas": {
                    "e": -43.18823478422753,
                    "g": 4.489207710979671e-05
                }
            },
            "rad2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.0075547270702817915,
                    "taus": 212.0558493893737
                },
                "Ra": 116.66549376685347,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 1.2054432876541832,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.006676979378995631,
                    "valf": -12.509171736433393
                },
                "pas": {
                    "e": -52.16771712825026,
                    "g": 5.663964256510521e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.02864511425205868,
                    "taus": 213.82290743717624
                },
                "Ra": 161.86087110491243,
                "cancr": {
                    "gcabar": 0.001272339818569152
                },
                "cm": 0.19000290878151518,
                "iCcr": {
                    "gkcbar": 0.002682049431287712
                },
                "kdrcr": {
                    "gkdrbar": 0.0027081909939373934,
                    "valf": -12.927293984218267
                },
                "pas": {
                    "e": -81.53814161804004,
                    "g": 2.7926922393979932e-05
                }
            }
        }

tunedParamsOrigBetterApril182025 = {
            "ori1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.03620051664945352,
                    "taus": 209.6402667869049
                },
                "Ra": 156.48488866793994,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.9862606024212732,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.007620749947248059,
                    "valf": -11.238475569220446
                },
                "pas": {
                    "e": -68.94520281296299,
                    "g": 4.9690008977514214e-05
                }
            },
            "ori2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.04637756634393874,
                    "taus": 195.75000066315047
                },
                "Ra": 149.16544292366643,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.894380975574114,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.001989049667110744,
                    "valf": -11.991581787070174
                },
                "pas": {
                    "e": -82.55328942703039,
                    "g": 5.9458077693878924e-05
                }
            },
            "rad1": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.0383372229380183,
                    "taus": 200.03659251492624
                },
                "Ra": 139.1751560040922,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 0.7800140087280175,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.0027802038807920797,
                    "valf": -15.416421652927266
                },
                "pas": {
                    "e": -39.834587008644164,
                    "g": 4.512702470327495e-05
                }
            },
            "rad2": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.007115974529340965,
                    "taus": 213.42669283460768
                },
                "Ra": 141.7078212258808,
                "cancr": {
                    "gcabar": 0.0
                },
                "cm": 1.207283724387104,
                "iCcr": {
                    "gkcbar": 0.0
                },
                "kdrcr": {
                    "gkdrbar": 0.006604210608652641,
                    "valf": -13.073161566111239
                },
                "pas": {
                    "e": -53.397303942965394,
                    "g": 5.481073970515329e-05
                }
            },
            "soma": {
                "IKscr": {
                    "gKsbar": 0.0
                },
                "Nafcr": {
                    "gnafbar": 0.029258105672312417,
                    "taus": 208.46441586035667
                },
                "Ra": 135.11537924391862,
                "cancr": {
                    "gcabar": 0.001200673446931951
                },
                "cm": 0.1762111618060807,
                "iCcr": {
                    "gkcbar": 0.002739309869536659
                },
                "kdrcr": {
                    "gkdrbar": 0.002731219341601073,
                    "valf": -11.792996540097391
                },
                "pas": {
                    "e": -74.63132881332893,
                    "g": 2.98701167732318e-05
                }
            }
        }

tunedParams = tunedParamsOrigBetterApril182025

cellRule = netParams.importCellParams(label='FoxP2', conds={'cellType': 'FoxP2', 'cellModel': 'HH_reduced'},
                                      fileName=cfg.hocFile, cellName='FoxP2', importSynMechs = True)

cellRule['secs']['soma']['mechs']['Nafcr']['gnafbar'] = tunedParams['soma']['Nafcr']['gnafbar']
cellRule['secs']['soma']['mechs']['Nafcr']['taus'] = tunedParams['soma']['Nafcr']['taus']
cellRule['secs']['soma']['mechs']['kdrcr']['gkdrbar'] = tunedParams['soma']['kdrcr']['gkdrbar']
cellRule['secs']['soma']['mechs']['kdrcr']['valf'] = tunedParams['soma']['kdrcr']['valf']
cellRule['secs']['soma']['mechs']['IKscr']['gKsbar'] = tunedParams['soma']['IKscr']['gKsbar']
cellRule['secs']['soma']['mechs']['iCcr']['gkcbar'] = tunedParams['soma']['iCcr']['gkcbar']
cellRule['secs']['soma']['mechs']['cancr']['gcabar'] = tunedParams['soma']['cancr']['gcabar']
cellRule['secs']['soma']['mechs']['pas']['e'] = tunedParams['soma']['pas']['e']
cellRule['secs']['soma']['geom']['cm'] = tunedParams['soma']['cm']
cellRule['secs']['soma']['geom']['Ra'] = tunedParams['soma']['Ra']
cellRule['secs']['soma']['mechs']['pas']['g'] = tunedParams['soma']['pas']['g']

for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
    cellRule['secs'][sec]['mechs']['Nafcr']['gnafbar'] = tunedParams[sec]['Nafcr']['gnafbar']
    cellRule['secs'][sec]['mechs']['Nafcr']['taus'] = tunedParams[sec]['Nafcr']['taus']
    cellRule['secs'][sec]['mechs']['kdrcr']['gkdrbar'] = tunedParams[sec]['kdrcr']['gkdrbar']
    cellRule['secs'][sec]['mechs']['kdrcr']['valf'] = tunedParams[sec]['kdrcr']['valf']
    cellRule['secs'][sec]['mechs']['IKscr']['gKsbar'] = tunedParams[sec]['IKscr']['gKsbar']
    cellRule['secs'][sec]['mechs']['iCcr']['gkcbar'] = tunedParams[sec]['iCcr']['gkcbar']
    cellRule['secs'][sec]['mechs']['cancr']['gcabar'] = tunedParams[sec]['cancr']['gcabar']
    cellRule['secs'][sec]['mechs']['pas']['e'] = tunedParams[sec]['pas']['e']
    cellRule['secs'][sec]['geom']['cm'] = tunedParams[sec]['cm']
    cellRule['secs'][sec]['geom']['Ra'] = tunedParams[sec]['Ra']
    cellRule['secs'][sec]['mechs']['pas']['g'] = tunedParams[sec]['pas']['g']

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
