from azioneAsincrona import azioneAsincrona

class Pircd(azioneAsincrona):
    def __init__(self):
        self.tempoAttuazione = 0.3
        self.tempoAttesa = 0.3

    def preCondizione(self,spazio,legal_moves,T1,T2,agent):
        if (spazio[agent][18] < T1 and spazio[agent][14] > T2 and spazio[agent][6] == 1 and spazio[agent][10] == 0 and 
            # Timer or noop difensore
            (spazio[agent][21] >=0 or spazio[agent][22] == 2)):
            legal_moves[4] = 1
        else:
            legal_moves[4] = 0

    def postCondizione(self,spazio,agent,T1,T2):
        print('TEMPOATTESA Pircd:',self.tempoAttesa)
        print('TEMPOATTUAZIONE Pircd:',self.tempoAttuazione)
        print('TEMPOATTESA/TEMPOATTUAZIONE Pircd:',self.tempoAttesa/self.tempoAttuazione)
        spazio[agent][18] = 1-(self.tempoAttesa/self.tempoAttuazione)
        