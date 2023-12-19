from azioneAsincrona import azioneAsincrona

class mossaAsincrona(azioneAsincrona):
    def __init__(self):
        self.tempoAttuazione = 1.0
        self.tempoAttesa = 1.0

    def preCondizione(self,spazio,legal_moves,mAttS,agent):
        if agent == 'attaccante':
            for i in range(mAttS):
                if spazio[agent][i] == 0 :
                    legal_moves[i] = 1
                else:
                    legal_moves[i] = 0
        else:
            for i in range(mAttS):
                if spazio[agent][i] == 0 :
                    legal_moves[i] = 0
                else:
                    legal_moves[i] = 1

    def postCondizione(self,spazio,agent):
        spazio[agent][16] = 1
