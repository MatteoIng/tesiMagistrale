from azioneAsincrona import azioneAsincrona
import random

# qui ho implementato la stessa idea delle mosse sincrone

class mossaAsincrona(azioneAsincrona):
    def __init__(self):
        self.tempoAttuazione = 1.0
        self.tempoAttesa = 1.0

    def preCondizione(self,spazio,legal_moves,pos,agent,mAttS):
        if agent == 'attaccante':
            
            for i in range(mAttS,len(legal_moves)):
                for j in range(mAttS,i):
                    print(f'POS {j} SPAZIO {spazio}')
                    if spazio['difensore'][j] == 0 :
                        legal_moves[pos] = 1
                        break
                    else:
                        legal_moves[pos] = 0
            else:
                legal_moves[pos] = 1
        else:
            
            for i in range(mAttS,len(legal_moves)):
                for j in range(mAttS,i):
                    print(f'POS {j} SPAZIO {spazio}')
                    if spazio[agent][i] == 1 :
                        legal_moves[pos] = 1
                        break
                    else:
                        legal_moves[pos] = 0



    def postCondizione(self,spazio,agent,action,mAttS):
        prob = round(random.random(),2)
        if agent == 'attaccante':
            #if prob <= 0.05 :
            for i in range(mAttS,(action+1)):
                spazio['difensore'][i] = 1
        else:    
            #if prob <= 0.1 :
            for i in range(mAttS,(action+1)):
                spazio['difensore'][i] = 0
        