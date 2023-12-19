from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class mossaSincrona(azioneSincrona):
    
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
    
    def postCondizione(self,spazio,agent,action):
        spazio[agent][action] = 1
