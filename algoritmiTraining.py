from pettingzoo.test import api_test, performance_benchmark
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig
from ray.rllib.algorithms.dqn import DQNConfig
from ray.rllib.algorithms.impala import ImpalaConfig
from ray.rllib.algorithms.pg import PGConfig
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env import PettingZooEnv
from ray.rllib.examples.models.action_mask_model import TorchActionMaskModel
from ray.rllib.models import ModelCatalog
from ray.rllib.utils import check_env
from ray.rllib.utils.framework import try_import_torch
from ray.tune.registry import register_env
# SERVE PER AVERE LO SPAZIO DELLE AZIONI DI DIMENSIONI DIVERSE
# e VOLENDO ANCHE LE OBSERVATIONs
from supersuit.multiagent_wrappers import (pad_action_space_v0,
                                           pad_observations_v0)

import rsp

env_name = "rsp"

# Definisco il mio ambiente
def env_creator():
        env = rsp.env(render_mode="human")
        return env

# Nome ambiente
env_name = "rsp"

# Registro il mio ambiente
register_env(env_name, lambda config: PettingZooEnv(pad_action_space_v0(env_creator())))
#register_env(env_name, lambda config: PettingZooEnv(pad_observations_v0(pad_action_space_v0(env_creator()))))

# Mi serve per usare l'action mask in odo da avere ad ogni step solo specifiche mosse
# senza dover gestire io mosse non selezionabili
ModelCatalog.register_custom_model("am_model", TorchActionMaskModel)

# Mi servono per il check e l'inizializzazione degli algoritmi
test_env = PettingZooEnv(pad_action_space_v0(env_creator()))
obs_space = test_env.observation_space
act_space = test_env.action_space

# Verifico l'ambiente così ch se faccio modifiche me lo dice senza fare il running e l'inizializzazione degli algoritmi
check_env(test_env)


class DQN:
    def __init__(self):

        self.config = (
    DQNConfig()
    .environment(
            env=env_name
    ).resources(num_gpus=1,num_cpus_for_local_worker=2)
    .rollouts(
            num_rollout_workers=3,
            rollout_fragment_length=10
    ).multi_agent(
            policies={
                    "attaccante": (None, obs_space, act_space, {}),
                    "difensore": (None, obs_space, act_space, {}),
                },
            policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).debugging(
            log_level="DEBUG"
    ).framework(
            framework="torch"
    ).exploration(
            exploration_config={
                    # The Exploration class to use.
                    "type": "EpsilonGreedy",
                    # Config for the Exploration class' constructor:
                    "initial_epsilon": 0.1,
                    "final_epsilon": 0.0,
                    "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
                }
    ).training(
            model = { 
                    "custom_model": "am_model", 
                },
    )#.callbacks(MyCallbacks)
)


class ApexDQN:
     def __init__(self):
          self.config = (
    ApexDQNConfig()
    .environment(
            env=env_name
    ).resources(num_gpus=1,num_cpus_for_local_worker=2)
    .rollouts(
            num_rollout_workers=3,
            ollout_fragment_length=10
    ).training(
            train_batch_size=200,
            model = { 
                    "custom_model": "am_model",
                }
    ).multi_agent(
            policies={
                    "attaccante": (None, obs_space, act_space, {}),
                    "difensore": (None, obs_space, act_space, {}),
            },
            policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).debugging(
    ).framework(
            framework="torch"
    ).exploration(
            exploration_config={
                    # The Exploration class to use.
                    "type": "EpsilonGreedy",
                    # Config for the Exploration class' constructor:
                    "initial_epsilon": 0.1,
                    "final_epsilon": 0.0,
                    "epsilon_timesteps": 100000,  # Timesteps over which to anneal epsilon.
            }
    )
)


# Strano l'attaccante si addestra a scegliere nop e poi difensore -log e finisce, non vorrei che minimizzasse 
# Però se così fosse il difensore non terminerebbe subito
class Impala():
     def __init__(self):
          self.config = (
      ImpalaConfig()
      .environment(env_name,disable_env_checking=True)
      .resources(num_gpus=1,num_cpus_for_local_worker=2)
      .framework("torch")
      .multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                "custom_model": "am_model"
                },
    ).rollouts(
            num_rollout_workers=3,
            rollout_fragment_length=10
    )
)
          
# Con 100 training iteration ho visto che le partite terminano con il difensore che in una media di 50 mosse vince
# PER ora tra PPO con 50 e Impala con 40 lui con 100 è il migliore (piu o meno il tempo di addstramento è stato lo stesso,
# se non quantop meno accettabile da attendere, perciò sono stati scelti questi valori di training non per 
# performance uguali)
class PG():
     def __init__(self):
          self.config = (
      PGConfig()
      .environment(env_name,disable_env_checking=True)
      .resources(num_gpus=1,num_cpus_for_local_worker=2)
      .framework("torch")
      .multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                "custom_model": "am_model"
                },
    ).rollouts(
            num_rollout_workers=3
    )
)  
          


# Con 50 epoche alcune le vince altre le perde, PG mi sembrava vincesse sempre (potrei sbagliare) pero partite piu brevi
class PPO():
     def __init__(self):
          self.config = (
      PPOConfig()
      .environment(env_name,disable_env_checking=True)
      # cpu_for_local_worker è per il training del ppo, devo capire quali per i rollout worker
      .resources(num_gpus=1,num_cpus_for_local_worker=2)
      .framework("torch")
      .multi_agent(
        policies={
            "attaccante": (None, obs_space, act_space, {}),
            "difensore": (None, obs_space, act_space, {}),
        },
        policy_mapping_fn=(lambda agent_id, *args, **kwargs: agent_id),
    ).training(
          model={
                "custom_model": "am_model"
                },
    ).rollouts(
            num_rollout_workers=3,
    )
)
          # PER IL CUSTOM MODEL ERROR
          self.config.rl_module( _enable_rl_module_api=False)
          self.config.training(_enable_learner_api=False)