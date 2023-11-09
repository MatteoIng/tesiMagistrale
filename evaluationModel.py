from ray import tune
from ray import train
from ray import air
import gymnasium

# path di un modello DQN trainato con 20 training iteration, che non so se equivalgono a 20 epoche
# 4095 episodi totali, ovvero mosse totali ottenute da tutte le partite
# num_env_steps_sampled 20400 non so cosa sia 
# num_env_steps_trained 20704 non so cosa sia
path = '/home/matteo/ray_results/DQN_2023-11-09_10-37-19/DQN_rsp_93b6e_00000_0_2023-11-09_10-37-19/checkpoint_000000'

############################################ PER VEDERLO GIOCARE #####################################
# Così va ma senza polisi sceglie random, ma va la logica della reward e dello stopping

from ray.rllib.algorithms.algorithm import Algorithm
algo = Algorithm.from_checkpoint(path)
algo.evaluate()

""" env = rsp.env(render_mode="human")
env.reset(seed=42)
action = 0

for agent in env.agent_iter():

    if len(env.agents)>1:
        print('\n')
        print('Seleziono agente:',agent)
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
        else:
            # this is where you would insert your polic
            mask = observation["action_mask"]
            action = env.action_space(agent).sample(mask)

        print('Osservazione:',observation)
        print('Azione selezionata da eseguire:',action)
        print('Reward accumulata:',reward)
        print('Termination:',termination)
        print('Troncation:',truncation)
        print('Step:')
        env.step(action)
    else:
        api_test(env, num_cycles=1000, verbose_progress=True)
        env.close()
        break

env.close() """