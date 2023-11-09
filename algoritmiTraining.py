import rsp

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



class DQN:
    def __init__(self):

        self.config = (
    DQNConfig()
    .environment(
            env=env_name
    ).resources(
            num_gpus=1 
    ).rollouts(
            num_rollout_workers=1,
            rollout_fragment_length=30
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
