from azioneAsincrona import azioneAsincrona
import random

# qui ho implementato la stessa idea delle mosse sincrone

class mossaAsincrona(azioneAsincrona):
    def __init__(self):
        self.tempoAttuazione = 1.0
        self.tempoAttesa = 1.0

    def preCondizione(self,spazio,legal_moves,pos,agent):
        if agent == 'attaccante':
            #for i in range(mAttS,mAttA,1):
            if spazio['difensore'][pos] == 1 :
                legal_moves[pos] = 0
            else:
                legal_moves[pos] = 1
        else:
            #for i in range(mAttS,mAttA,1):
            if spazio[agent][pos] == 0 :
                legal_moves[pos] = 0
            else:
                legal_moves[pos] = 1

    def postCondizione(self,spazio,agent,action):
        prob = round(random.random(),2)
        if agent == 'attaccante':
            if prob <= 0.05 :
                spazio['difensore'][action] = 1
        else:    
            if prob <= 0.1 :
                spazio[agent][action] = 0
        