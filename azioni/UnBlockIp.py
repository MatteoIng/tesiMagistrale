#from azioneSincrona import azioneSincrona
from azioneAsincrona import azioneAsincrona
import time

class UnBlockIp(azioneAsincrona):
    def preCondizione():
        pass
    def postCondizione(self,spazio,agent):
        spazio[agent][1] = 0
