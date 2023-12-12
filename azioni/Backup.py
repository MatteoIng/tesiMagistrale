
from azioneAsincrona import azioneAsincrona
import time

class Backup(azioneAsincrona):
    def __init__(self):
        self.tempoAttuazione = 0.5
        self.tempoAttesa = 0.5

    def preCondizione(self,spazio,legal_moves,T1,T2,agent,mosseAsincroneRunning):
        if (spazio[agent][6] == 1 and spazio[agent][9] == 0 and spazio[agent][7] == 0 and
            spazio[agent][3] == 1 and spazio[agent][5] > 1 and spazio[agent][0] == 1 and 
            # Timer or noop attaccante
            (spazio[agent][21] <= 0 or spazio[agent][22] == 1) and
            (spazio[agent][15] > T1 or spazio[agent][16] > T1 or spazio[agent][17] > T1 or 
             spazio[agent][18] > T1 or spazio[agent][19] > T1 or spazio[agent][20] > T1)
             and 16 not in mosseAsincroneRunning):
            legal_moves[16] = 1
        else:
            legal_moves[16] = 0

    def postCondizione(self,spazio,agent,T1,T2):
        if (self.tempoAttesa/self.tempoAttuazione) <= 0:
            spazio[agent][9] = 1
            print('BACKUP TERMINATO ORA')
