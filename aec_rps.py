import functools

import gymnasium
import numpy as np
from gymnasium.spaces import Discrete, Dict, Box

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
import fantasyBoard



# Mosse 
MOVES = ['mossa1', 'mossa2','mossa3']

# Questa è la truncation cosi esce per non girare all'infinito
NUM_ITERS = 20

# Mappa che in base all'azione eseguita mi da costo, impatto, ecc dell'azione
REWARD_MAP = {
    'mossa1': (1, 0, 0),
    'mossa2': (2, 0, 0),
    'mossa3': (3, 0, 0)
}

# per la funzione di reward
wt = 0.5
wc = 0.5
wi = 0.5
tMax = 100
cMax = 100



def env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env



class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gymnasium, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human"], "name": "rps_v2"}

    def __init__(self, render_mode=None):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - render_mode

        Note: as of v1.18.1, the action_spaces and observation_spaces attributes are deprecated.
        Spaces should be defined in the action_space() and observation_space() methods.
        If these methods are not overridden, spaces will be inferred from self.observation_spaces/action_spaces, raising a warning.

        These attributes should not be changed after initialization.
        """
################################################## AGENTI ##############################################################
        self.possible_agents = ['attaccante','difensore']
        self._agent_ids = set(self.possible_agents)
        # per ogni agente mette le azioni ovvero tante quante le mosse
        # Discrete lo usa per generare uno random con sample()
        self._action_spaces = {agent: Discrete(3) for agent in self.possible_agents}
        
############################################# Spazio -> Stato ##########################################################
        # per ogni agente mette lo spazio degli stati 4 (3 delle mosse e None)
        # io dovrei forse definire una classe, 1 stato oggetto, poi le configurazioni internre sono gli stati
        self._observation_spaces = {
            agent:dict(
                {
                    # observation dovrebbe avere i parametri dello stato,
                    # è lo spazio e lo stato è dato dalla config dei suoi parametri
                    # ho preso 2 dove mossa 1 accende spegne il 1 e mossa due uguale
                    # Box mi genera una lista e mi controlla nel limiti low and high 
                    'observation': [False,False,False],

                    # stessa dimensione delle mosse per selezionare mosse non selezionabili
                    # 2 mosse
                    #
                    #'observation' : Box(low=0,high=1,shape=(3,))
                    #"action_mask": [True,True]
                }
            )
            for agent in self.possible_agents
        }
        

        self.render_mode = render_mode
        print('Action spaces:',self._action_spaces)
        print('Observation:',self._observation_spaces)

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return self._observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self._action_spaces[agent]

    def render(self):
        
        #Renders the environment. In human mode, it can print to terminal, open
        #up a graphical window, or open up some other display that a human can see and understand.

        if self.render_mode is None:
            gymnasium.logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return

        """ if len(self.agents) == 2:
            string = "Current state: Agent1: {} , Agent2: {}".format(
                MOVES[self.state[self.agents[0]]], MOVES[self.state[self.agents[1]]]
            )
        else:  """
        string = "Game over"    
        
        
        print('rendering....') 

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self._observation_spaces[agent])

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - terminations
        - truncations
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.
        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
############################################### QUando termina a me ? ###################################################        
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        #self.state = {agent: NONE for agent in self.agents}
        #self.observations = {agent: NONE for agent in self.agents}

        # credo serve per arrestare
        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()
        return 

    def step(self, action):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations
        - truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            # handles stepping an agent which is already dead
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next dead agent,  or if there are no more dead agents, to the next live agent
            self._was_dead_step(action)
            print('ECCOOOO:',self.agents)
            return

        agent = self.agent_selection
        print('Agente in azione:',agent)

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        #self._cumulative_rewards[agent] = 0

        # stores action of current agent
        #self.state[self.agent_selection] = action

        # collect rewarewardsrd if it is the last agent to act
        #if self._agent_selector.is_last():
            # rewards for all agents are placed in the .rewards dictionary

############################################### REWARD ##################################################################
# Nella Reward map c'è valore d'impatto della mossa, che viene ussata per calcolare la reward
        reward = REWARD_MAP[MOVES[action]]
        valReward = -wt*(reward[0]/tMax)-wc*(reward[1]/cMax)-wi*(1) 
        #rewardInv = -valReward
        print('Reward:',valReward)
        if self.agent_selection == 'attaccante':
            self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (valReward,0)
        else:
            self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (0,valReward)
        
##################################Dovrei inserire le pre / post condizioni delle azioni #######################################
        print('Prima della mossa:',self._observation_spaces)
        if action == 0:
            self._observation_spaces[self.agent_selection]['observation'][action]=True
        elif action == 1:
            self._observation_spaces[self.agent_selection]['observation'][0]=True
            self._observation_spaces[self.agent_selection]['observation'][action]=True
        elif action == 2:
            self._observation_spaces[self.agent_selection]['observation'][0]=True
            self._observation_spaces[self.agent_selection]['observation'][1]=True
            self._observation_spaces[self.agent_selection]['observation'][action]=True
        print('Dopo la mossa:',self._observation_spaces)

############################################# Condizione di arresto #####################################################
# da modificare ma capire come, Truncation; In realta puo restare cosi perchè deve arrestare per termination
# ma se non riessce va bene anche cosi
        self.num_moves += 1
        # The truncations dictionary must be updated for all players.
        self.truncations = {
            agent: self.num_moves >= NUM_ITERS for agent in self.agents
        }
        # se uno degli agenti è in uno stato di tutti True esce 
        self.terminations = {
            agent: True if all(item == True for item in self._observation_spaces[agent]['observation']) else False for agent in self.agents
        }
        print('Deve terminare?',self.terminations)
########################################################################################################################
        # observe the current state
        """ for i in self.agents:
            self.observations[i] = self.state[
                self.agents[1 - self.agent_name_mapping[i]]
            ] """
        """ else:
            # necessary so that observe() returns a reasonable observation at all times.
            self.state[self.agents[1 - self.agent_name_mapping[agent]]] = 'None'
            # no rewards are allocated until both players give an action
            self._clear_rewards()"""
        
        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

        if self.render_mode == "human":
            self.render()