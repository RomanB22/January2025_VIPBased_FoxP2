from netpyne.batchtools.search import search

NoiseMultiplier = 1 # 1e-10 (or whatever small number larger than zero) or 1 to use the In-vivo background noise
AMPA_weight = 0.004 # 0.004 for 200 pA of EPSC driven by a NetStim in soma, 0.008 for 400 pA of EPSC
# Since Rin in the model is twice as large than experiment, we use half of the weights,
# to compensate that effect on the membrane potential

params = {'IClamp1.amp': [-0.2, 0, 0.2],
          'NetStimRatePre': [NoiseMultiplier*6.7],#[0, 6.7]
          'NetStimRatePost': [NoiseMultiplier*6.7*0.87], #[0, 6.7*0.87], # 6.7+3*4.7=20.8 Hz
          'NetStimNoise': [0.71],
          'NetStimWeight': [AMPA_weight],
          'AMPANMDAWeightsIncre': [AMPA_weight],
          'AMPANMDAWeightsDecre': [AMPA_weight],
          'AMPANMDAWeightsNotChanging': [AMPA_weight],
          'delay': [2], # ?
          'IncreConn': [int(18*0.5), 18, 18*2, 18*3, 18*4, 18*5], # 25% Incre - 65% Decre
          'DecreConn': [int(51*0.5), 51, 51*2, 51*3, 51*4, 51*5], #
          'NotChangingConn': [4], # ? 5-10%
          'synsPerConn': [1, 3],#[1, 3], # ?
          'Condition': ['InVivo_Go', 'OnlyIncre_Go', 'MirrorDecre_Go']
          }

# use batch_shell_config if running directly on the machine
shell_config = {'command': 'nrniv -python src/init.py',}

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
       output_path = './data/results_%s_%s' % (AMPA_weight, int(NoiseMultiplier)),
       checkpoint_path = './data/ray_%s_%s' % (AMPA_weight, int(NoiseMultiplier)),
       run_config = run_config,
       num_samples = 1,
       algorithm = "variant_generator",
       metric = 'loss',
       mode = 'min',
       max_concurrent = 10)