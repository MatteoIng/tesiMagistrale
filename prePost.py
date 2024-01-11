from matplotlib import pyplot as plt
import numpy as np
import random

from Attaccante import Attaccante
from Difensore import Difensore

from threading import Thread

attaccante = Attaccante()
difensore = Difensore()

T1 = 0.33
T2 = 0.66


# qui per ogni partita mette numero di mosse fatte e le cumulative reward finali di quella partita
reward_mosse = {
    "attaccante":[(0,0)],
    "difensore":[(0,0)]
}

# qui mette tutte le reward di ogni partita, le cumulative reward, ovvero i contatori
curva_partita = {
    "attaccante": [],
    "difensore":[],
}



# Pre condizioni codificate nell'action mask
def preCondizioni(agent,spazio,legal_moves,mosse,timer):
    # STATO

    if agent == 'difensore':
        # pre condizioni del difensore
        difensore.preCondizioni(spazio,legal_moves,mosse,agent,timer)

    else:
        # pre condizioni dell'attaccante
        # In tutte ho inserito che se il software viene aggiornato neanche più il pscan si può fare 
        # altrimenti non ce la farebbe mai ad uscire perche deve decrementare i log
        attaccante.preCondizioni(spazio,legal_moves,mosse,agent,timer)
        

    if agent == 'difensore':
        print('-----------------------------------------------------------------------------------------')
        print(legal_moves)
        
    else :
        print('-----------------------------------------------------------------------------------------')
        print(legal_moves)
        



# APPLICA L'AZIONE ALLo SPAZIO 'LOGICA'
def postCondizioni(action,spazio,agent,mosse,timer,lastTimer):
    # Post COndizioni
    mossaValida = True

    if agent == 'difensore':
        lastTimer = difensore.postCondizioni(action,spazio,agent,mosse,timer,lastTimer)
        
    elif agent == 'attaccante':
        lastTimer = attaccante.postCondizioni(action,spazio,agent,mosse,timer,lastTimer)

    return lastTimer
        




# VERIFICA QUANDO CALCOLARE LA REWARD, NEGLI ALTRI CASI 0
def reward(agent,action,mosse,n_azioni,n_azioni_attaccante_asincrone,n_azioni_difensore_asincrone):
    # per la funzione di reward
    calcolo = 0
    val = action
    if agent == 'attaccante':
        # cosi la prima sincrona ha lo stesso costo della prima asincrona
        if action > n_azioni_attaccante_asincrone:
            val = action-n_azioni_attaccante_asincrone

        if action < mosse[agent]['sincrone']:
            calcolo = attaccante.reward(attaccante.REWARD_MAP[0])/((n_azioni+1)/(val+1))
        else:
            calcolo = attaccante.reward(attaccante.REWARD_MAP[0])/((n_azioni+1)/(val+1))
    else:
        # cosi la prima sincrona ha lo stesso costo della prima asincrona
        if action > n_azioni_difensore_asincrone:
            val = action-n_azioni_difensore_asincrone

        if action < mosse[agent]['sincrone']:
            calcolo = -(difensore.reward(difensore.REWARD_MAP[0])/((n_azioni+1)/(val+1)))
        else:
            calcolo = -(difensore.reward(difensore.REWARD_MAP[0])/((n_azioni+1)/(val+1)))
    return calcolo



# CONTROLLA LO STATE PER TERMINAR EO MENO
def terminationPartita(spazio,lm,num_moves,NUM_ITERS):
    val = False

    # clean system state + esclusione degli altri parametri (lascio solo il check degli attacchi sotto T1 
    # come se gli altri fossero altri subsets states con minace in sicurezza)
    # stato terminale attaccante con tutti attacchi on
    # Consigliata dal professore
    checkNot = [not(spazio['difensore'][i]) for i in range(len(spazio['difensore'])-1)]
    check = spazio['difensore'][:(len(spazio['difensore'])-1)]
    if (#all(check) or 
        all(checkNot)):
        val = True
    else:
            # se non puo arrestarlo neanche quello provo a vedere il num di mosse
            # con noOp sempre selezionabili mi dovrebbe uscire con la condizione nell'if
            if num_moves >= NUM_ITERS:
                val = True
    return val


# Randomicità dello stato
def generazioneSpazioRandom(dim_obs):
    # STATO [x+yVar + timer]
    # STATO CHE AVEVO SUPPOSTO IO DI PARTENZA
    #spazio = [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    spazio = []
    for i in range(dim_obs-1):
        spazio.append(random.randint(0,1))
    # timer
    spazio.append(0)


    return spazio

def reset():
    attaccante.reset()
    difensore.reset()
