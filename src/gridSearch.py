from netpyne.batchtools.search import search

DepolBlock = 'False'

params = {'IAmp': [0],
          'depolBlockModel': [DepolBlock],
          'NoiseMultiplier': [1],
          'NetStimNoise': [0.71],
          'NetStimRateProportion': [0.87], #[0, 0.87, 1] # Percentage of background noise after movement with respect to preparation
          'AMPA_weight': [0.002], # Same for all connections. ? Unknown variable
          'delay': [3.8], # 3.8
          'IncreConn': [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32], # 25% Incre - 65% Decre
          'DecreConn': [0, 1, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42], #
          'NotChangingConn': [0], # ? Unknown variable. Fixed to 5-10%
          'synsPerConn': [1], # ? Unknown variable
          'Condition': ['InVivo_Go', 'OnlyIncre_Go', 'MirrorDecre_Go']
          }
# If you don't want to save the figures for all the gridsearch, uncomment following line
# params['analysis'] = [{}]

# use batch_shell_config if running directly on the machine
shell_config = {'command': 'nrniv -python src/init.py'}

# use batch_sge_config if running on a SunGrid Engine
sge_config = {
    'queue': 'cpu.q',
    'cores': 1,
    'vmem': '4G',
    'realtime': '00:10:00',
    'command': 'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py'}

run_config = shell_config

search(job_type = 'sh', # or 'sh'
       comm_type = 'socket',
       label = 'grid',
       params = params,
       output_path = './data/gridsearch_Dep%s' % DepolBlock,
       checkpoint_path = './data/ray_Dep%s' % DepolBlock,
       run_config = run_config,
       num_samples = 1,
       algorithm = "variant_generator",
       max_concurrent = 10)