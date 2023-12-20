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

#mosseDifensore = ['Generate alert','FirewallActivation','BlockSourceIp','UnblockSourceIp','FlowRateLimit','UnlimitFlowRate',
#                  'RedirectToHoneypot','UnRedirectToHoneypot','IncreaseLog','DecreaseLog','QuarantineHost','UnQuarantineHost',
#                  'ManualResolution','SystemReboot','SystemShutdown','SystemStart','BackupHost','SoftwareUpdate','noOp']

#mosseAttaccante = ['Pscan','Pvsftpd','Psmbd','Pphpcgi','Pircd','Pdistccd','Prmi', 'noOp']


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
        # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
        # log_verb([0-5])(5),
        # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
        # updated([True/False])(10),
        # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
        # +
        # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),]

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
def postCondizioni(action,spazio,agent,mosse,timer):
    # Post COndizioni
    # STATO
    # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
    # log_verb([0-5])(5),
    # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
    # updated([True/False])(10),
    # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
    # +
    # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),]

    mossaValida = True

    if agent == 'difensore':
        difensore.postCondizioni(action,spazio,agent,mosse,timer)
        
    elif agent == 'attaccante':
        attaccante.postCondizioni(action,spazio,agent,mosse,timer)
        




# VERIFICA QUANDO CALCOLARE LA REWARD, NEGLI ALTRI CASI 0
def reward(agent,action,mosse):
    # per la funzione di reward
    calcolo = 0
    if agent == 'attaccante':
        if action < mosse[agent]['sincrone']:
            calcolo = attaccante.reward(attaccante.REWARD_MAP[0])
        else:
            calcolo = attaccante.reward(attaccante.REWARD_MAP[1])
    else:
        if action < mosse[agent]['sincrone']:
            calcolo = -attaccante.reward(attaccante.REWARD_MAP[0])
        else:
            calcolo = -attaccante.reward(attaccante.REWARD_MAP[1])
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
    if (all(check) or all(checkNot)):
        val = True
    else:
            # se non puo arrestarlo neanche quello provo a vedere il num di mosse
            # con noOp sempre selezionabili mi dovrebbe uscire con la condizione nell'if
            if num_moves >= NUM_ITERS:
                val = True
    return val


# Randomicità dello stato
def generazioneSpazioRandom(dim_obs):
    # STATO
        # [ firewall([True/False])(0), blockedip([])(1), flowlimit_ips([])(2), alert([True/False])(3), honeypot_ips([])(4),
        # log_verb([0-5])(5),
        # active([True/False])(6), quarantined([True/False])(7), rebooted([True/False])(8), backup([True/False])(9),
        # updated([True/False])(10),
        # manuallySolved([True/False])(11), everQuarantined([True/False])(12), everShutDown([True/False])(13),
        # +
        # pscan([0-1])(14), pvsftpd([0-1])(15), psmbd([0-1])(16), pphpcgi([0-1])(17), pircd([0-1])(18), pdistccd([0-1])(19), prmi([0-1])(20),
        # timer(21),noop(22)]
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
