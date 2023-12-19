from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

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
        if agent == 'attaccante':
            spazio['difensore'][action] = 1
        else:    
            spazio['difensore'][action] = 0
        


