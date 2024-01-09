from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time
import random 

# Nel paper abbiamo che l'attaccante incrementa un contatore con una probabilità di 0.05 (5%??)
# il difensore lo decrementa con una probabilita di 1/10 (10%?)
# ogni azione sincrona corrisponde una componente nello spazio
# l'attaccante riesce nell'attacco con una probabilità pari al 5%
# il difensore al 10%

class mossaSincrona(azioneSincrona):
    
    def preCondizione(self,spazio,legal_moves,mAttS,agent):
        if agent == 'attaccante':
            for i in range(mAttS):
                if spazio['difensore'][i] == 0 :
                    legal_moves[i] = 1
                else:
                    legal_moves[i] = 0
        else:
            for i in range(mAttS):
                if spazio[agent][i] == 1 :
                    legal_moves[i] = 1
                else:
                    legal_moves[i] = 0
    
    def postCondizione(self,spazio,agent,action):
        
        soglia = round(random.random(),2)

        if agent == 'attaccante':
                for i in range(action):
                    # probabilità per ogni mossa
                    #prob = round(random.random(),2)
                    #if prob <= soglia :
                    spazio['difensore'][i] = 1
        else:    
            for i in range(action):
                    # probabilità per ogni mossa
                    #prob = round(random.random(),2)
                    #if prob <= soglia :
                    spazio['difensore'][i] = 0
        


