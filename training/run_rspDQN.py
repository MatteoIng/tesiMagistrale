# se lancio dalla cartella principale
import sys

sys.path.append('./')

import time

import ray
from pettingzoo.test import api_test, performance_benchmark
from ray import air, train, tune
from ray.rllib.algorithms.algorithm import Algorithm
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.algorithms.dqn import DQNConfig
from ray.rllib.algorithms.impala import ImpalaConfig
from ray.rllib.algorithms.pg import PGConfig
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env import PettingZooEnv
from ray.rllib.examples.models.action_mask_model import TorchActionMaskModel
from ray.rllib.models import ModelCatalog
from ray.rllib.utils import check_env
from ray.rllib.utils.framework import try_import_torch
from ray.tune import Stopper
from ray.tune.registry import register_env
# SERVE PER AVERE LO SPAZIO DELLE AZIONI DI DIMENSIONI DIVERSE
# e VOLENDO ANCHE LE OBSERVATIONs
from supersuit.multiagent_wrappers import (pad_action_space_v0,
                                           pad_observations_v0)

import rsp
from algoritmiTraining import DQN, PG, PPO, ApexDQN, Impala
from visualizzazione import visualizza_reward_mosse

# NEI RESULT TROVIAMO:
# episode_length NUMERO DEI TURNI PRIMA DELLA TERMINAZIONE (1 SOLO ATTACCANTE, 2 ATTACCANTE+DIFENSORE ...)
# policy_*_reward METTE SOLO LE REWARD OTTENUTE DALL'AGENTE QUANDO VINCE
# episode_reward È LA SOMMA DELLE REWARD ATTACCANTE E DIFENSORE (AD OGNI TURNO NE VINCE UNO SOLO)
# MI SON FATTO UN RESULT TUTTO MIO CUSTOM, PER ORA SCRIVE SUL FILE MA MODIFICABILE



torch, nn = try_import_torch()
torch.cuda.empty_cache()

trainingIteration =  int(sys.argv[1])
g = float(sys.argv[1])

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
#############################################################################################
###############################################  DQN  #######################################
#############################################################################################

config = DQN().config

# Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
config['hiddens'] = []
config['dueling'] = False

# per l'evaluation
config['evaluation_interval'] = 1

algo = config.training(gamma=g).build()

results = tune.Tuner(
    "DQN",
    run_config = train.RunConfig(stop=stop,verbose=1),
    param_space = config,
).fit()

visualizza_reward_mosse() 

