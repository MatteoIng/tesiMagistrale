import random
from threading import Thread

import numpy as np
from matplotlib import pyplot as plt

from Attaccante import Attaccante
from Difensore import Difensore

attaccante = Attaccante()
difensore = Difensore()

T1 = 0.33
T2 = 0.66


# qui per ogni partita mette numero di mosse fatte e le cumulative reward finali di quella partita
reward_mosse = {
    "attaccante":[],
    "difensore":[]
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
        lastTimer = difensore.postCondizioni(action,spazio,agent,mosse,timer)
        
    elif agent == 'attaccante':
        lastTimer = attaccante.postCondizioni(action,spazio,agent,mosse,timer)

    return lastTimer
        




# VERIFICA QUANDO CALCOLARE LA REWARD, NEGLI ALTRI CASI 0
def reward(agent,action,spazioDiff,n_azioni,n_azioni_attaccante_sincrone,n_azioni_difensore_sincrone,waitPosition):
    # per la funzione di reward
    calcolo = 0
    val = action
    if agent == 'attaccante':
        # cosi la prima sincrona ha lo stesso costo della prima asincrona
        #if action > n_azioni_attaccante_asincrone:
        """ val = action-n_azioni_attaccante_sincrone
        print(f'VAL MOSSA ASINCRONA {val}') """

        #if action < mosse[agent]['sincrone']:
            #calcolo = attaccante.reward(attaccante.REWARD_MAP[0])/((n_azioni+1)/(action+1))
        calcolo = attaccante.reward(action,n_azioni)
        #calcolo = (action+1 - n_azioni)/ n_azioni
        """ else:
            #calcolo = attaccante.reward(attaccante.REWARD_MAP[0])/((n_azioni+1)/(val+1))
            calcolo = (action+1 - n_azioni)/ n_azioni """
    else:
        # cosi la prima sincrona ha lo stesso costo della prima asincrona
        #if action > n_azioni_difensore_asincrone:
        """ val = action-n_azioni_difensore_sincrone
        print(f'VAL MOSSA ASINCRONA {val}') """

        #if action < mosse[agent]['sincrone']:
            #calcolo = -(difensore.reward(difensore.REWARD_MAP[0])/((n_azioni+1)/(action+1)))
        #calcolo = (action+1 - n_azioni)/ n_azioni

        if action != waitPosition and action != waitPosition+1:
            mossaRewardMinore = -1
            for i in range(len(spazioDiff)-1):
                if spazioDiff[i] == 1:
                    mossaRewardMinore = i  

            actionPerReward = action-mossaRewardMinore
            if mossaRewardMinore > action:
                actionPerReward = mossaRewardMinore-action
            print('ACTIONPERREWARD:',actionPerReward)

            calcolo = -((actionPerReward+1)/ (n_azioni))
        else:
            calcolo = 0
        """ else:
            #calcolo = -(difensore.reward(difensore.REWARD_MAP[0])/((n_azioni+1)/(val+1)))
            calcolo = (action+1 - n_azioni)/ n_azioni """
    return calcolo



# CONTROLLA LO STATE PER TERMINAR EO MENO
def terminationPartita(spazio,legal_moves,num_moves,NUM_ITERS,mAtt,mDiff):
    val = False
    
    # clean system state + esclusione degli altri parametri (lascio solo il check degli attacchi sotto T1 
    # come se gli altri fossero altri subsets states con minace in sicurezza)
    # stato terminale attaccante con tutti attacchi on
    # Consigliata dal professore
    checkNot = [not(spazio['difensore'][i]) for i in range(len(spazio['difensore'])-1)]
    check = spazio['difensore'][:(len(spazio['difensore'])-1)]

    #lenMAtt = attaccante.lenMosseEseguite()
    #lenMDiff = difensore.lenMosseEseguite()
    mosseDisp = False
    for i in range(mAtt):
        if legal_moves[i] == 1:
            mosseDisp = True

    lenMAAtt = attaccante.lenMosseAsincroneRunning()
    lenMAADiff = difensore.lenMosseAsincroneRunning()

    #print('checkNot:',checkNot)
    #print('check:',check)
    #print(f'lenMAtt:{lenMAtt} e mAtt:{mAtt}',)
    #print(f'lenMDiff:{lenMDiff} e mDiff:{mDiff}')


    if ( all(checkNot) or (mosseDisp and lenMAADiff == 0 and (1 in check))): #or (lenMAtt == mAtt and lenMAAtt == 0 and lenMDiff == mDiff and lenMAADiff == 0)):
    #if ((all(checkNot) and lenMAtt == mAtt) or (lenMDiff == mDiff and (1 in check)) or (lenMAtt == mAtt and lenMAAtt == 0 and lenMDiff == mDiff and lenMAADiff == 0)):
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
        #spazio.append(random.randint(0,1))
        spazio.append(0)
    spazio.append(0)
    # altero random una componente simulando un attacco 
    spazio[random.randint(0,dim_obs-1)] = 1


    return spazio

def reset():
    attaccante.reset()
    difensore.reset()
