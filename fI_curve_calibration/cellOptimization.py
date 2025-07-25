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
def evolCellFoxP2(algo='optuna', min=0.9, max=1.1):
    # parameters space to explore
    # min and max are the percentage variation for the limits of the search space.
    # TunedParams are based on previous optimization using 'evol' algorithm
    params = specs.ODict()
    tunedParams = {
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

    # valf = -13#-35
    # taus = 1000
    # factoIkslow_soma = 0
    # factoCalcium_soma = 1
    # factoIkslow_dend = 0
    # factoCalcium_dend = 0
    #
    # params[('tune', 'soma', 'Nafcr', 'gnafbar')] = [1e-3, 5e-2]
    # params[('tune', 'soma', 'Nafcr', 'taus')] = [taus*0.99, taus*1.01]
    #
    # params[('tune', 'soma', 'kdrcr', 'gkdrbar')] = [1e-3, 1e-2]
    # params[('tune', 'soma', 'kdrcr', 'valf')] = [valf*1.1, valf*0.9]
    #
    # params[('tune', 'soma', 'IKscr', 'gKsbar')] = [factoIkslow_soma*1e-5, factoIkslow_soma*1e-4]
    #
    # params[('tune', 'soma', 'iCcr', 'gkcbar')] = [factoCalcium_soma*1e-3, factoCalcium_soma*1e-2]
    #
    # params[('tune', 'soma', 'cancr', 'gcabar')] = [factoCalcium_soma*1e-3, factoCalcium_soma*1e-2]
    #
    # params[('tune', 'soma', 'pas', 'e')] = [-90, -40]
    # params[('tune', 'soma', 'cm')] = [0.1, 0.5]
    # params[('tune', 'soma', 'Ra')] = [100, 300]
    # params[('tune', 'soma', 'pas', 'g')] = [1e-5, 4e-5]
    #
    # for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
    #     params[('tune', sec, 'Nafcr', 'gnafbar')] = [1e-3, 5e-2]
    #     params[('tune', sec, 'Nafcr', 'taus')] = [taus*0.99, taus*1.01]
    #
    #     params[('tune', sec, 'kdrcr', 'gkdrbar')] = [1e-3, 1e-2]
    #     params[('tune', sec, 'kdrcr', 'valf')] = [valf*1.1, valf*0.9]
    #
    #     params[('tune', sec, 'IKscr', 'gKsbar')] = [factoIkslow_dend*1e-5, factoIkslow_dend*1e-4]
    #
    #     params[('tune', sec, 'iCcr', 'gkcbar')] = [factoCalcium_dend*1e-3, factoCalcium_dend*1e-2]
    #
    #     params[('tune', sec, 'cancr', 'gcabar')] = [factoCalcium_dend*1e-3, factoCalcium_dend*1e-2]
    #
    #     params[('tune', sec, 'pas', 'e')] = [-90, -40]
    #     params[('tune', sec, 'cm')] = [0.6, 1.3]
    #     params[('tune', sec, 'Ra')] = [100, 300]
    #     params[('tune', sec, 'pas', 'g')] = [4e-5, 7e-5]

    offset = 0
    for sec in ['soma', 'rad1', 'rad2', 'ori1', 'ori2']:
        tunedParams[sec]['Ra'] = 150

    params[('tune', 'soma', 'Nafcr', 'gnafbar')] = [tunedParams['soma']['Nafcr']['gnafbar']*min, tunedParams['soma']['Nafcr']['gnafbar']*max]
    params[('tune', 'soma', 'Nafcr', 'taus')] = [tunedParams['soma']['Nafcr']['taus']*min, tunedParams['soma']['Nafcr']['taus']*max]

    params[('tune', 'soma', 'kdrcr', 'gkdrbar')] = [tunedParams['soma']['kdrcr']['gkdrbar']*min, tunedParams['soma']['kdrcr']['gkdrbar']*max]
    params[('tune', 'soma', 'kdrcr', 'valf')] = [tunedParams['soma']['kdrcr']['valf']*max, tunedParams['soma']['kdrcr']['valf']*min]

    params[('tune', 'soma', 'IKscr', 'gKsbar')] = [tunedParams['soma']['IKscr']['gKsbar']*min, tunedParams['soma']['IKscr']['gKsbar']*max]

    params[('tune', 'soma', 'iCcr', 'gkcbar')] = [tunedParams['soma']['iCcr']['gkcbar']*min, tunedParams['soma']['iCcr']['gkcbar']*max]

    params[('tune', 'soma', 'cancr', 'gcabar')] = [tunedParams['soma']['cancr']['gcabar']*min, tunedParams['soma']['cancr']['gcabar']*max]

    params[('tune', 'soma', 'pas', 'e')] = [tunedParams['soma']['pas']['e']*max-offset, tunedParams['soma']['pas']['e']*min-offset]
    params[('tune', 'soma', 'cm')] = [tunedParams['soma']['cm']*min, tunedParams['soma']['cm']*max]
    params[('tune', 'soma', 'Ra')] = [tunedParams['soma']['Ra']*min, tunedParams['soma']['Ra']*max]
    params[('tune', 'soma', 'pas', 'g')] = [tunedParams['soma']['pas']['g']*min, tunedParams['soma']['pas']['g']*max]

    for sec in ['rad1', 'rad2', 'ori1', 'ori2']:
        params[('tune', sec, 'Nafcr', 'gnafbar')] = [tunedParams[sec]['Nafcr']['gnafbar']*min, tunedParams[sec]['Nafcr']['gnafbar']*max]
        params[('tune', sec, 'Nafcr', 'taus')] = [tunedParams[sec]['Nafcr']['taus']*min, tunedParams[sec]['Nafcr']['taus']*max]

        params[('tune', sec, 'kdrcr', 'gkdrbar')] = [tunedParams[sec]['kdrcr']['gkdrbar']*min, tunedParams[sec]['kdrcr']['gkdrbar']*max]
        params[('tune', sec, 'kdrcr', 'valf')] = [tunedParams[sec]['kdrcr']['valf']*max, tunedParams[sec]['kdrcr']['valf']*min]

        params[('tune', sec, 'IKscr', 'gKsbar')] = [tunedParams[sec]['IKscr']['gKsbar'] * min,
                                                       tunedParams[sec]['IKscr']['gKsbar'] * max]

        params[('tune', sec, 'iCcr', 'gkcbar')] = [tunedParams[sec]['iCcr']['gkcbar'] * min,
                                                      tunedParams[sec]['iCcr']['gkcbar'] * max]

        params[('tune', sec, 'cancr', 'gcabar')] = [tunedParams[sec]['cancr']['gcabar'] * min,
                                                       tunedParams[sec]['cancr']['gcabar'] * max]

        params[('tune', sec, 'pas', 'e')] = [tunedParams[sec]['pas']['e']*max-offset, tunedParams[sec]['pas']['e']*min-offset]
        params[('tune', sec, 'cm')] = [tunedParams[sec]['cm']*min, tunedParams[sec]['cm']*max]
        params[('tune', sec, 'Ra')] = [tunedParams[sec]['Ra']*min, tunedParams[sec]['Ra']*max]
        params[('tune', sec, 'pas', 'g')] = [tunedParams[sec]['pas']['g']*min, tunedParams[sec]['pas']['g']*max]

    # initial cfg set up
    initCfg = {} # specs.ODict()
    initCfg['saveDataInclude'] = ['simData']
    # initCfg[('analysis', 'plotTraces')] = {}

    for k, v in params.items():
        initCfg[k] = v[0]  # initialize params in cfg so they can be modified

    # Fitting average fI curve
    with open('cells/AverageProperties.pkl', 'rb') as f:
        average_props = pickle.load(f)
    steps = 1
    # end=1
    # amps = average_props['f-I Curve'][0][0][::steps]
    targetRates = average_props['f-I Curve'][0][1][::steps]
    # targetRatesStd = average_props['f-I Curve Std'][0][1][::steps]
    # amps = [10 / 1000. * i for i in range(61)]

    # Fitting Bikoff 2016 published trace
    # targetRates = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.298850575, 6.896551724, 9.195402299,
    #                11.49425287, 13.79310345, 16.09195402, 16.09195402, 18.3908046, 20.68965517, 22.98850575,
    #                22.98850575, 25.28735632, 27.5862069, 27.5862069, 27.5862069, 29.88505747, 32.18390805, 32.18390805,
    #                34.48275862, 36.7816092, 36.7816092, 39.08045977, 39.08045977, 39.08045977, 41.37931034, 41.37931034,
    #                43.67816092, 43.67816092, 45.97701149, 45.97701149, 45.97701149, 48.27586207, 48.27586207,
    #                50.57471264, 50.57471264, 50.57471264, 52.87356322, 52.87356322, 52.87356322, 52.87356322]

    # fitness function
    fitnessFuncArgs = {}
    fitnessFuncArgs['target'] = {'rates': targetRates}
    fitnessFuncArgs['maxFitness'] = 2000

    def fitnessFunc(simData, **kwargs):
        targetRates = kwargs['target']['rates']
        diffRates = [abs(x-t) for x,t in zip(simData['fI'], targetRates)]
        fitness = np.mean(diffRates)
        # To avoid very negative membrane resting potentials
        if np.min(simData['V_soma']['cell_0'])<(-85*1.1) or np.min(simData['V_soma']['cell_0'])>(-85*0.9): fitness = kwargs['maxFitness']
        if np.sum([x for x in simData['fI']])<10: fitness = kwargs['maxFitness']
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
            'maxiters': 3000,  # Maximum number of iterations (1 iteration = 1 function evaluation)
            'maxtime': None,  # Maximum time allowed, in seconds
            'maxiter_wait': 5,
            'time_sleep': 5,
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
    algo='optuna'
    b = evolCellFoxP2(algo=algo, min=0.9, max=1.1) # Choose optimization algorithm: 'evol', 'optuna'
    b.batchLabel = '%sfI_Jan2025_Final_2' % algo
    b.saveFolder = 'data/' + b.batchLabel
    setRunCfg(b, 'mpi_bulletin')
    b.run()  # run batch

    #LAST THING I DID WAS TO ADD IKSCR INN DENDRITES-MAYBE NOT GOOD IDEA