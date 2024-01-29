import sys
# se lancio dalla cartella principale
sys.path.append(r'./')

from  visualizzazione import visualizza_reward_mosse

from algoritmiTraining import PG 


import rsp

import ray
import time

from ray import tune
from ray import train
from ray import air

from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.algorithms.algorithm import Algorithm
from ray.tune import Stopper

from ray.rllib.algorithms.impala import ImpalaConfig
from ray.rllib.algorithms.pg import PGConfig
from ray.rllib.algorithms.dqn import DQNConfig
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig


from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils import check_env

from ray.rllib.examples.models.action_mask_model import TorchActionMaskModel

from ray.tune.registry import register_env

from ray.rllib.models import ModelCatalog

from ray.rllib.env import PettingZooEnv

from pettingzoo.test import api_test
from pettingzoo.test import performance_benchmark





# SERVE PER AVERE LO SPAZIO DELLE AZIONI DI DIMENSIONI DIVERSE
# e VOLENDO ANCHE LE OBSERVATIONs
from supersuit.multiagent_wrappers import pad_action_space_v0,pad_observations_v0


# NEI RESULT TROVIAMO:
# episode_length NUMERO DEI TURNI PRIMA DELLA TERMINAZIONE (1 SOLO ATTACCANTE, 2 ATTACCANTE+DIFENSORE ...)
# policy_*_reward METTE SOLO LE REWARD OTTENUTE DALL'AGENTE QUANDO VINCE
# episode_reward È LA SOMMA DELLE REWARD ATTACCANTE E DIFENSORE (AD OGNI TURNO NE VINCE UNO SOLO)
# MI SON FATTO UN RESULT TUTTO MIO CUSTOM, PER ORA SCRIVE SUL FILE MA MODIFICABILE



torch, nn = try_import_torch()
torch.cuda.empty_cache()

trainingIteration =  int(sys.argv[1])

# COndizioni di stopping degli algoritmi 
stop = {
        # epoche/passi dopo le quali il training si arresta
        "training_iteration": trainingIteration,

        #"timesteps_total":2,

        # passi ambientali dell'agente nell'ambiente
        # ci sarebbe un minimo di 200
        #"timesteps_total": 2,

        # ferma il training quando la ricompensa media dell'agente nell'episodio è pari o maggiore
        #"episode_reward_max": 5,
    }

# RAY  VIENE UTILIZZATO PER POTER FARE IL TUNING DEGLI IPERPARAMETRI
# SI PUO DEFINIRE UN RANGE ED IN AUTOMATICA FA I DIVERSI TRAINING CON LE DIVERSE CONFIG
#ray.shutdown()
#ray.init()



################################################# RAY #######################################

############################################################################################
##############################################  PG  ########################################
############################################################################################
# Policy gradient
# vanilla policy gradients using experience collected from the latest interaction with the agent implementation 
# (using experience collected from the latest interaction with the agent)

config = PG().config

config['evaluation_interval'] = 1
config['create_env_on_driver'] = True
# per l'evaluation
config['evaluation_interval'] = 1


algo = config.build()

results = tune.Tuner(
        "PG",
        param_space=config, 
        run_config=air.RunConfig(stop=stop, verbose=1)
    ).fit() 
    
visualizza_reward_mosse()

