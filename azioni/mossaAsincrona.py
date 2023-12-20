from azioneAsincrona import azioneAsincrona

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
        if agent == 'attaccante':
            spazio['difensore'][action] = 1
        else:    
            spazio['difensore'][action] = 0
