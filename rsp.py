import functools
import json
import numpy as np

from gymnasium.spaces import Discrete,Box,Dict

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from prePost import postCondizioni,reward,terminationPartita,reward_mosse,curva_partita,preCondizioni,generazioneSpazioRandom,reset


import sys
import os

# metto una copia delle legal moves così che lastmossa è nop solo se era l'unica disponibile

# 7 attacchi (pscan,pvsftpd,psmbd,pphpcgi,pircd,pdistccd,prmi) hanno una probabilità con tui il difensore lo valuta
# 0 < T1 < T2 < 1 e p < T1 rumore, T1 < p < T2 possibile attacco (prevenzione), p > T2 attacco by IDS (contromisure),
# p=1 attacco noto e strategia da attuare
# Lo stato del difensore è composto da: 7 p (una per ogni attacco) + 14 variabili di sistema,
# presumibilmente l'attaccante ora vede tutto per un taining più efficace

# il difensore ha 18 azioni, 21 componenti nello stato 
# l'attaccante ne ha 7, lo stato esamina quello del difensore 
# considererei lo stato clean quello di partenza e lo stato target una configurazione delle anomalie innocua (DA DEFINIRE BENE)
# per l'attaccante qual'è lo stato target di vittoria??

# PER ORA:
# ATTACCANTE 
# azioni : 3 (come gli attacchi).. IMPEGANTIVO OGNI VOLTA STARE A CODIFICARE UNO SCENARIO
# lo spazio monitora quello del difensore
# VINCE: per semplicità metto per ora che 2 mossE PER FARE BINGO (0 e 2: 0 da 0 a 6 e 6 da 6 a 14)

# DIFENSORE
# azioni : 14 (sono dippiù perche 1 azioni può modificare più variabili ma per ora facciamo 1 azione 1 variabile)
# 14 attributi -> observation (nel paper non tutti true/false per ora 14 bool)
# VINCE: quando spazio TUTTI TRUE, ma credo che punti a non morire mai

# L'OTTIMO PER IL DIFENSORE E FAR SALIRE SEMPRE LA REWARD PERCHE NON MUORE E RIESCE SEMPRE A DIFENDERSI
# L'ATTACCANTE DEVE TROVARE SUBITO LA COMBO VINCENTE (2 MOSSE)

# E LE SUE REWARD DIMINUISCONO COL TEMPO, PERCHÈ SE IL DIFENSORE NEL CASO OTTIMO IN AL PIÙ 13 MOSSE VINCEREBBE
# PERCHE TUTTI FALSE UN SOLO TRUE, L'ATTACCANTE SCEGLIE SEMPRE LA MOSSA DOVE HA GIA FALSE, E AD OGNI SUO TURNO
# SCEGLIE UNA MOSSA BUONA CHE GLI CAMBIA UNA VARIABILE, 
# CREDO CHE PERDA SEMPRE PER QUESTO MOTIVO, OTTIENE PIU REWARD SE RESISTE PIUTTOSTO CHE VINCERE)

#------------------------------------- Lettura conf ---------------------------------#
conf = open("conf.txt", "r")
lines = conf.readlines()
for i in range(len(lines)-1):
    lines[i] = int(lines[i].strip().split('= ')[1])

n_agenti = int(lines[0])
print(f'Numero agenti : {n_agenti}')

n_azioni_attaccante_sincrone = int(lines[2])
print(f'Mosse sincrone dell attaccante: {n_azioni_attaccante_sincrone}')

n_azioni_attaccante_asincrone = int(lines[2])
print(f'Mosse asincrone dell attaccante: {n_azioni_attaccante_asincrone}')

n_azioni_difensore_sincrone = int(lines[2])
print(f'Mosse sincrone del difensore: {n_azioni_difensore_sincrone}')

n_azioni_difensore_asincrone = int(lines[2])
print(f'Mosse asincrone del difensore: {n_azioni_difensore_asincrone}')

# dimensione dello stato, tutte variabili booleane + timer 
dim_obs = 0
# azioni attaccante e dfensore uguali, + noop (ma in numero sincrone ed asincrone puo variare)
n_azioni = 0
# posizione del timer nello spazio
timer = 0
if ((n_azioni_attaccante_sincrone+n_azioni_attaccante_asincrone) == (n_azioni_difensore_sincrone+n_azioni_difensore_asincrone)):
    # ogni azione una var dello stato + timer
    dim_obs = n_azioni_attaccante_sincrone + n_azioni_attaccante_asincrone + 1
    # mosse totali somma asincrone e sincrone + noop
    n_azioni = n_azioni_attaccante_sincrone + n_azioni_attaccante_asincrone +1
    # set timer
    timer = dim_obs - 1

else:
    # esce se in numero tot le mosse dell'attaccante e del difensore non sono uguali
    sys.exit('la somma delle azioni sincrone ed asincrone di ciascun agente deve essere la stessa')

mosse = {
    'attaccante':{
        'sincrone':n_azioni_attaccante_sincrone,
        'asincrone':n_azioni_attaccante_asincrone,
    },
    'difensore':{
        'sincrone':n_azioni_difensore_sincrone,
        'asincrone':n_azioni_difensore_asincrone,
    }
}

#-------------------------------------- Lettura conf ----------------------------------#

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

        # Questa è la truncation cosi esce per non girare all'infinito
        self.NUM_ITERS = 10

        # Lo utilizzo affinche termini quando entrambi i due agenti, in maniera conseutiva hanno a disposizione
        # solo mosse noop selezionabili:
        # nmosse è il numero di mossa della partita in cui hanno solo noop
        # in mosse salvo l'actionmask per la verifica
        # nmosse lo uso per la sequenzialità dei noop-noop

        #self.possible_agents = [f'agente{i}' for i in range(n_agenti)]
        self.possible_agents = ['attaccante','difensore']

        self.lm = {
            i:{
                'nmosse':-1,
                'mosse':[]
            } for i in self.possible_agents
        }

        # spazio del difensore monitorato anche dall'attaccante per l'observation dopo un'action
        self.spazio = {
            i: generazioneSpazioRandom(dim_obs)
            for i in self.possible_agents
        }
        
        # STATO
        # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
        # log_verb([0-5])(5),
        # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
        # updated([True/False])(10),
        # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
        # +
        # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),
        # timer(21),noop(22)]

        # per ora non lo sto usando lo spazio dell'attaccante
        #self.spazio[self.possible_agents[0]] = [False]
        # Mi serve solo per rimuovere un wrap per usare il dizionario per l'action mask MA NON LO STO USANDO

        print('Spazii:',self.spazio)

        # optional: a mapping between agent name and ID
        """ self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        ) """

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        # SOLITAMENTE ALGORITMI ACCETTANO TUTTI DISCRETE, 1 VAL 1 MOSSA
        self._action_spaces = {}
        

        """ self._action_spaces = {
                Discrete(n_azioni_) for i in self.possible_agents
            } """
    
        # ATTACCANTE: attacchi=[Pscan(0), Pvsftpd(1), Psmbd(2), Pphpcgi(3), Pircd(4), Pdistccd(5), Prmi(6), noOp(7)]
        self._action_spaces[self.possible_agents[0]] = Discrete(n_azioni)

        # DIFENSORE: 18 azioni= [GenerateAlert(0), FirewallActivation(1), BlockSourceIp(2), UnblockSourceIp(3),
        # FlowRateLimit(4), UnlimitFlowRate(5), RedirectToHoneypot(6), UnHoneypot(7), IncreaseLog(8),
        # DecreaseLog(9), QuarantineHost(10), UnQuarantineHost(11), ManualResolution(12), SystemReboot(13),
        # SystemShutdown(14), SystemStart(15), BackupHost(16), SoftwareUpdate(17), noOp(18)]
        self._action_spaces[self.possible_agents[1]] = Discrete(n_azioni)

        # DEVE ESSERE DELLA STESSA STRUTTURA DEL RITORNO DI observe() 
        self._observation_spaces = {}
        # lo spazio dell'attaccante per ora non viene utilizzato
        # Me ne basta uno solo

        # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
        # log_verb([0-5])(5),
	    # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
        # updated([True/False])(10),
	    # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
	    # +
	    # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),]

        #N = len(self.spazio['difensore'])

        self._observation_spaces = {
            i : Dict(
                {
                    "observations": Box(low=-1000, high=1000, shape=(dim_obs,), dtype=float),
                    "action_mask": Box(low=0, high=1, shape=(n_azioni,), dtype=np.int8),
                }
            ) for i in self.possible_agents
        }
        
                    
        self.render_mode = render_mode


# SE NON ERRO OBS_SPACE E ACT_SPACE VENGONO UTILIZZATI ALL'INIZIO PER FAR SI CHE LA DEFINIZIONE DI TUTTO QUADRI
# PERCHÈ REALMENTE NEL CODICE NON VENGONO UTILIZZATI, OBBLIGATORI MA NON UTILIZZATI
    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        print('QUI')
        return self._observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        print('QUO')
        return self._action_spaces[agent]

    def render(self):
        print('')

# INVECE MOLTO IMPORTANTE OBSERVE CHE FA TORNRE L'OSSERVAZIONE IN BASE ALLA MOSSA
# IN FATTI STO USANDO LA VARIABILE SPAZIO CHE ERA SATATA PROGETTATA PER LA MIA LOGICA INTERNA, IL COMPORTAMENTO
    def observe(self, agent):
        # PRE CONDIZIONI

        # STATO
        # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
        # log_verb([0-5])(5),
	    # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
        # updated([True/False])(10),
	    # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
	    # +
	    # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),]

        # SERVE A FAR SI CHE IN UNO STATO ALCUNE AZIONI NON SIANO SELEZIONABILI

        # DIFENSORE AZIONI
        # [GenerateAlert(0), FirewallActivation(1), BlockSourceIp(2), UnblockSourceIp(3), FlowRateLimit(4), UnlimitFlowRate(5), 
		# RedirectToHoneypot(6), UnHoneypot(7), IncreaseLog(8), DecreaseLog(9), QuarantineHost(10), UnQuarantineHost(11),
		# ManualResolution(12), SystemReboot(13), SystemShutdown(14), SystemStart(15), BackupHost(16), SoftwareUpdate(17),
        # noOp(18)]
        
        # ATTACCANTE AZIONI
        #[Pscan(0), Pvsftpd(1), Psmbd(2), Pphpcgi(3), Pircd(4), Pdistccd(5), Prmi(6), noOp(7)]
        legal_moves = np.zeros(n_azioni,'int8')

        preCondizioni(agent,self.spazio,legal_moves,mosse,timer)
        self.lm[agent]['mosse'] = np.copy(legal_moves)

        print('\t')
        print('Observe agent:',agent)
        print('Observe observation:',self.spazio['difensore'])
        print('Observe action mask/legal moves:',legal_moves)

        # in observation sto facendo tornare lo stato attuale ovvero spazio che uso per la mia logica interna,
        # dato che mi stabilisce sia reward e mossa
        # SIA ALL'ATTACCANTE CHE AL DIFENSORE STO FACENDO TORNARE LO STESSO SPAZIO COSÌ CHE
        # NE SIA PRESENTE UNO UNICO CONDIVISO E NON DUE REPLICATI
        #return np.stack(self.spazio['difensore'])
        # HO AGGIUNTO L'ACTION MASK PER IMPEDIRE LA SCELTA DI ALCUNE MOSSE PRECONDIZIONI
        return {
                'observations':np.stack(self.spazio['difensore']),
                'action_mask':np.stack(legal_moves),
                }
       

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass


    def reset(self, seed=None, options=None):
        # prePost Reset per attaccante e difensore
        reset()

        self.lm = {
            i:{
                'nmosse':-1,
                'mosse':[]
            } for i in self.possible_agents
        }

        # spazio del difensore monitorato anche dall'attaccante per l'observation dopo un'action
        self.spazio = {
            i: generazioneSpazioRandom(dim_obs)
            for i in self.possible_agents
        }
    
        self.agents = self.possible_agents[:]

        # CI SONO LE REWARD DI ENTRAMBI GLI AGENTI CHE VENGONO AGGIUNTE ALLE CUMULATIVE OGNI VOLTA CHE UNO DEI DUE 
        # FA UN'AZIONE: ATTACANTE AGISCE, GENERE 2 REWARD (ATT,DIFF) E LE METTE ALLE ACCUMULATIVE, TEMPORANEE
        self.rewards = {agent: 0 for agent in self.agents}

        # CI SONO TUTTE LE REWARD DI OGNI STEP, OVVERO DI OGNI VOLTA CHE UN AGENTE FA UN'AZIONE
        # DUE UNA PARTITA FINCHE NON ESCE UN VINCITORE
        self._cumulative_rewards = {agent: 0 for agent in self.agents}

        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}

        # ANCORA MAI USATO 
        self.infos = {agent: {} for agent in self.agents}

        # SE SERVE POTREI SALVARCI GLI STATI INTERMEDI DEL DIFF
        #self.state = {agent: NONE for agent in self.agents
        #self.observations = {agent: 3 for agent in self.agents}

        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()




    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            #or self.truncations[self.agent_selection]
        ):
            # DI OGNI PARTITA SALVO LE REWARD OTTENUTE TOTALI E IL NUMERO DI MOSSE ASSOCIATE
            reward_mosse[self.agent_selection].append((self.num_moves,self._cumulative_rewards[self.agent_selection]))
            
            # SALVOLE INFO NEI FILE
            # apro in write perche butto dentro la struttura dati in prePost
            # che mi tiene tutto ed alla fine ho i dati di tutto
            file_uno = open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/reward_mosse.txt", "w")
            #file_due = open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/curva_partita.txt", "w")
            file_uno.write(json.dumps(reward_mosse))
            #file_due.write(json.dumps(curva_partita))
            file_uno.close()
            #file_due.close()
            
            print('Action dead:',action)
            print('Rewards dead:',self._cumulative_rewards)
            self._was_dead_step(action)
            return
        
        
        agent = self.agent_selection
        #print('Agente in azione:',agent)
        print('Mossa da eseguire:',action)
        print('Timer Prima:',self.spazio['difensore'][timer])

        ######################## PRE(con action mask solo post)/POST condizioni #####################################################

        #print('Prima della mossa:',self.spazio)
        postCondizioni(action,self.spazio,self.agent_selection,mosse,timer)
        self.spazio['difensore'][timer] = round(self.spazio['difensore'][timer],3)
        print('Dopo la mossa:',self.spazio['difensore'])

        ############################################## REWARD ###########################################

        # SI INFLUENZANO LE REWARD A VICENDA
        """ print('Mossa valida:',mossaValida)
        if mossaValida: """
        rw = reward(agent,action,mosse)
        #if agent == 'difensore':
        self.rewards[agent] += rw
        """ else:
            self.rewards[agent] -= rw """
        
        ############################# CHECK ARRESTO (se sono nello stato sicuro) #########################
        
        # COSA STO FACENDO
        # NOOP-NOOP MI TERMINA
        # MASOLO NEL CASO FOSSERO LE ULTIME DUE MOSSE RIMASTE
        # VOGLIO VEDERE SE MIGLIORA IL TRAINING
        # aggiungo la sequenialità delle noop-noop mel'ero dimenticataa

        if agent == 'attaccante':
            # solo noop puo fare se true
            att = [not(i) for i in self.lm['attaccante']['mosse']]
            #print('att:',att)
            if all(att[:7]):
                #print('ENTRATOatt')
                self.lm[agent]['nmosse'] = self.num_moves
        else:
            # solo noop puo fare se true
            diff = [not(i) for i in self.lm['difensore']['mosse']]
            #print('diff:',diff)
            if all(diff[:18]):
                #print('ENTRATOdiff')
                self.lm[agent]['nmosse'] = self.num_moves


        # NON POSSONO AVERE VALORI DISCORDI GLI AGENTI delle terminations e troncation
        val = terminationPartita(self.spazio,self.lm,self.num_moves,self.NUM_ITERS)
        # se la condizione di aresto generale lo ferma bene altrimenti...
        self.terminations = {
            agent: val for agent in self.agents
        }

        ##################################################################################################
        
        # SALVE TUTTE LE REWARD CUMULATIVE DI TUTTE LE PARTITE
        #curva_partita['attaccante'].append((self.num_moves,self._cumulative_rewards['attaccante']))
        #curva_partita['difensore'].append((self.num_moves,self._cumulative_rewards['difensore']))

        self._accumulate_rewards()

        print('Timer Dopo:',self.spazio['difensore'][timer])
        print('Num Mosse:',self.num_moves)
        print('Truncation:',self.truncations)
        print('Termination:',self.terminations)
        print('Rewards:', self.rewards)
        print('reward cumulative:',self._cumulative_rewards)

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        self.num_moves += 1
        self.rewards[agent] = 0
        
        if self.render_mode == "human":
            self.render()
