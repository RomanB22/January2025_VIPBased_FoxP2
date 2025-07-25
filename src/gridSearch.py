from netpyne.batchtools.search import search

Fitting = 'False'
TwoStims = 'False'
ConstantArea = 'False'
SecondMov = 250 # 500, 250, 1000
Conditions = ['InVivo_Go', 'MirrorDecre_Go', 'OnlyIncre_Go', 'LowVar_Go', 'HighVar_Go', 'NoVar_Go'] #['InVivo', 'OnlyIncre', 'MirrorDecre', 'LowVar', 'HighVar']
folderSave = './ChangeVar_2' #'./dataExpInputs'

factorAmp = [1.] #[0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
factorWidth = [1.] #[0.5, 1, 2]

IncDecConstantN = [(0,2),(1,1),(2,0),
                   (0,3),(1,2),(2,1),(3,0),
                   (0,8),(1,7),(2,6),(3,5),(4,4),(5,3),(6,2),(7,1),(8,0),
                   (0,14),(1,13),(2,12),(3,11),(4,10),(5,9),(6,8),(7,7),
                   (8,6),(9,5),(10,4),(11,3),(12,2),(13,1),(14,0),
                   (0,20),(1,19),(2,18),(3,17),(4,16),(5,15),(6,14),(7,13),(8,12),(9,11),(10,10),
                   (11,9),(12,8),(13,7),(14,6),(15,5),(16,4),(17,3),(18,2),(19,1),(20,0)]

Nmax = 10
step = 1
IncDecGrid = [(i,j) for i in range(0,Nmax+step,step) for j in range(0,Nmax+step,step)]

params = {'IAmp': [0],
          'NoiseMultiplier': [1],
          'NetStimNoise': [0.71], # deprecated
          'NetStimRateProportion': [0.87], #[0, 0.87, 1] # Percentage of background noise after movement with respect to preparation
          'AMPA_weight': [0.00025], # Same for all connections. ? Unknown variable
          'delay': [3.8], # 3.8
          'IncDec': IncDecGrid,
          'NotChangingConn': [0], # ? Unknown variable. Fixed to 5-10%
          'synsPerConn': [1], # ? Unknown variable
          'Condition': Conditions, # OnlyIncre_Go
          'factorAmp': factorAmp,
          'factorWidth': factorWidth,
          'Fitting': [Fitting],
          'TwoStims': [TwoStims],
          'SecondStimDelay': [SecondMov],
          'ConstantArea': [ConstantArea],
          'blockNa': ['False']
          }
# If you don't want to save the figures for all the gridsearch, uncomment following line
# params['analysis'] = [{}]

# use batch_shell_config if running directly on the machine
shell_config = {'command': 'nrniv -python src/init.py'}

run_config = shell_config

search(job_type = 'sh', # or 'sh'
       comm_type = 'socket',
       label = 'grid', # 'optuna'
       params = params,
       output_path = folderSave+'/g_F%s_A%s' % (Fitting[0], ConstantArea[0]),
       checkpoint_path = folderSave+'/r_F%s_A%s' % (Fitting[0], ConstantArea[0]),
       run_config = run_config,
       num_samples = 1,
       algorithm = "variant_generator",
       max_concurrent = 5)