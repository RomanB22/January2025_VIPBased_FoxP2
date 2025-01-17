from netpyne.batchtools.search import search

DepolBlock = 'True'

params = {'IAmp': [0],
          'depolBlockModel': [DepolBlock],
          'NoiseMultiplier': [1],
          'NetStimNoise': [0.71],
          'NetStimRateProportion': [0.87], #[0, 0.87, 1] # Percentage of background noise after movement with respect to preparation
          'AMPA_weight': [0.001, 0.002, 0.003, 0.004], # Same for all connections. ? Unknown variable
          'delay': [2], # [1, 2, 3, 4] ? Unknown variable
          'IncreConn': [int(18*0.25), int(18*0.5), int(18*0.75), 18, int(18*1.25), int(18*1.5), int(18*1.75), int(18*2), int(18*2.25), int(18*2.5)], # 25% Incre - 65% Decre
          'DecreConn': [int(51*0.25), int(51*0.5), int(51*0.75), 51, int(51*1.25), int(51*1.5), int(51*1.75), int(51*2), int(51*2.25), int(51*2.5)], #
          'NotChangingConn': [4], # ? Unknown variable. Fixed to 5-10%
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