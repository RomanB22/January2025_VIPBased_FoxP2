"""
batch.py

Batch simulation for M1 model using NetPyNE

Contributors: salvadordura@gmail.com
"""
import numpy as np
import netpyne
from netpyne import specs
from netpyne.batch import Batch
import pickle

import os

# ---------------------------------------------------------------------------------------------- #
# -----                              f-I curve calibration                                ------ #
# ---------------------------------------------------------------------------------------------- #
def evolCellFoxP2(algo='optuna', min=0.1, max=2, depolBlockModel=True):
    # parameters space to explore
    # min and max are the percentage variation for the limits of the search space.
    # TunedParams are based on previous optimization using 'evol' algorithm
    params = specs.ODict()
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
    if depolBlockModel:
        tunedParams = tunedParamsDepol
    else:
        tunedParams = tunedParamsNoDepol

    [tunedParams['soma']['Nafcr']['gnafbar']*min, tunedParams['soma']['Nafcr']['gnafbar']*max]

    params[('tune', 'soma', 'Nafcr', 'gnafbar')] = [tunedParams['soma']['Nafcr']['gnafbar']*min, tunedParams['soma']['Nafcr']['gnafbar']*max]
    params[('tune', 'soma', 'kdrcr', 'gkdrbar')] = [tunedParams['soma']['kdrcr']['gkdrbar']*min, tunedParams['soma']['kdrcr']['gkdrbar']*max]
    params[('tune', 'soma', 'IKscr', 'gKsbar')] = [tunedParams['soma']['IKscr']['gKsbar']*min, tunedParams['soma']['IKscr']['gKsbar']*max]
    params[('tune', 'soma', 'iCcr', 'gkcbar')] = [tunedParams['soma']['iCcr']['gkcbar']*min, tunedParams['soma']['iCcr']['gkcbar']*max]
    params[('tune', 'soma', 'cancr', 'gcabar')] = [tunedParams['soma']['cancr']['gcabar']*min, tunedParams['soma']['cancr']['gcabar']*max]
    # params[('tune', 'soma', 'pas', 'e')] = [-95, -70]
    # params[('tune', 'soma', 'cm')] = [1.3*min, 1.3*max]
    params[('tune', 'soma', 'Ra')] = [100, 200]
    # params[('tune', 'soma', 'pas', 'g')] = [2e-4*min, 2e-4*max]

    for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
        params[('tune', sec, 'Nafcr', 'gnafbar')] = [tunedParams[sec]['Nafcr']['gnafbar']*min, tunedParams[sec]['Nafcr']['gnafbar']*max]
        params[('tune', sec, 'kdrcr', 'gkdrbar')] = [tunedParams[sec]['kdrcr']['gkdrbar']*min, tunedParams[sec]['kdrcr']['gkdrbar']*max]
        # params[('tune', sec, 'pas', 'e')] = [-95, -70]
        # params[('tune', sec, 'cm')] = [1*min, 1*max]
        params[('tune', sec, 'Ra')] = [100, 200]
        # params[('tune', sec, 'pas', 'g')] = [1e-4*min, 1e-4*max]

    # initial cfg set up
    initCfg = {} # specs.ODict()
    initCfg['saveDataInclude'] = ['simData']
    initCfg['depolBlockModel'] = depolBlockModel
    # initCfg[('analysis', 'plotTraces')] = {}

    for k, v in params.items():
        initCfg[k] = v[0]  # initialize params in cfg so they can be modified

    # Fitting average fI curve
    # with open('cells/AverageProperties.pkl', 'rb') as f:
    #     average_props = pickle.load(f)
    # steps = 1
    # end=1
    # amps = average_props['f-I Curve'][0][0][::steps]
    # targetRates = average_props['f-I Curve'][0][1][::steps]
    # targetRatesStd = average_props['f-I Curve Std'][0][1][::steps]
    # amps = [10 / 1000. * i for i in range(61)]

    # Fitting Bikoff 2016 published trace
    targetRates = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.298850575, 6.896551724, 9.195402299,
                   11.49425287, 13.79310345, 16.09195402, 16.09195402, 18.3908046, 20.68965517, 22.98850575,
                   22.98850575, 25.28735632, 27.5862069, 27.5862069, 27.5862069, 29.88505747, 32.18390805, 32.18390805,
                   34.48275862, 36.7816092, 36.7816092, 39.08045977, 39.08045977, 39.08045977, 41.37931034, 41.37931034,
                   43.67816092, 43.67816092, 45.97701149, 45.97701149, 45.97701149, 48.27586207, 48.27586207,
                   50.57471264, 50.57471264, 50.57471264, 52.87356322, 52.87356322, 52.87356322, 52.87356322]

    # fitness function
    fitnessFuncArgs = {}
    fitnessFuncArgs['target'] = {'rates': targetRates}
    fitnessFuncArgs['maxFitness'] = 2000

    def fitnessFunc(simData, **kwargs):
        targetRates = kwargs['target']['rates']
        diffRates = [abs(x-t) for x,t in zip(simData['fI'], targetRates)]
        fitness = np.mean(diffRates)
        # To avoid very negative membrane resting potentials
        if np.min(simData['V_soma']['cell_0'])<-91: fitness = kwargs['maxFitness']
        # TODO: Add extra high amplitude to explore depolarization blockade

        print(' Candidate rates: ', simData['fI'])
        print(' Target rates:    ', targetRates)
        print(' Difference:      ', diffRates)

        return fitness

    # create Batch object with parameters to modify, and specifying files to use
    b = Batch(cfgFile='fI_curve_calibration/cfg.py', netParamsFile='fI_curve_calibration/netParams.py',
              params=params, initCfg=initCfg)

    b.method = algo
    if b.method=='optuna':
        b.optimCfg = {
            'fitnessFunc': fitnessFunc,  # fitness expression (should read simData)
            'fitnessFuncArgs': fitnessFuncArgs,
            'maxFitness': 1000,
            'maxiters': 1e6,  # Maximum number of iterations (1 iteration = 1 function evaluation)
            'maxtime': None,  # Maximum time allowed, in seconds
            'maxiter_wait': 5,
            'time_sleep': 10,
            'popsize': 1  # unused - run with mpi
        }
    elif b.method=='evol':
        # Set evol method (all param combinations)
        b.evolCfg = {
            'evolAlgorithm': 'custom', #'custom',2
            'fitnessFunc': fitnessFunc, # fitness expression (should read simData)
            'fitnessFuncArgs': fitnessFuncArgs,
            'pop_size': 100,
            'num_elites': 2, # keep this number of parents for next generation if they are fitter than children
            'mutation_rate': 0.5,
            'crossover': 0.5,
            'maximize': False, # maximize fitness function?
            'max_generations': 30,
            'time_sleep': 50, # wait this time before checking again if sim is completed (for each generation)
            'maxiter_wait': 5, # max number of times to check if sim is completed (for each generation)
            'defaultFitness': 1000 # set fitness value in case simulation time is over
        }
    else:
        print("Unknown optimization algorithm")
        quit()

    return b
# ----------------------------------------------------------------------------------------------
# Run configurations
# ----------------------------------------------------------------------------------------------
def setRunCfg(b, type='mpi_bulletin'):
    if type=='mpi_bulletin':
        b.runCfg = {'type': 'mpi_bulletin',
            'script': 'fI_curve_calibration/init.py',
            'skip': False
                    }#'skipCustom': '_data.json'}

    elif type=='mpi_direct':
        b.runCfg = {'type': 'mpi_direct',
            'cores': 1,
            'script': 'fI_curve_calibration/init.py',
            'mpiCommand': 'mpiexec',
            'nrnCommand': 'nrniv -python',
            'skip': False,
            'skipCustom': '_data.pkl'}

    elif type=='hpc_sge':
        b.runCfg = {'type': 'hpc_sge',
                    'jobName': 'my_batch',
                    'cores': 1,
                    'mpiCommand': 'mpiexec',
                    'vmem': '1G',
                    'walltime': "00:30:00",
                    'script': 'fI_curve_calibration/init.py',
                    'queueName': 'cpu.q',
                    'skip': False,
                    'skipCustom': '_data.json'}
# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Single cell calibration
    algo='evol'
    depolBlockModel = False
    b = evolCellFoxP2(algo=algo, depolBlockModel=False) # Choose optimization algorithm: 'evol', 'optuna'
    b.batchLabel = '%sfI_Jan2025_Depol%s' % (algo, depolBlockModel)
    b.saveFolder = 'data/' + b.batchLabel
    setRunCfg(b, 'mpi_bulletin')
    b.run()  # run batch