from Agente import Agente

from azioni.Pscan import Pscan
from azioni.Pvsftpd import Pvsftpd
from azioni.Psmbd import Psmbd
from azioni.Pphpcgi import Pphpcgi
from azioni.Pircd import Pircd
from azioni.Pdistccd import Pdistccd
from azioni.Prmi import Prmi
from azioni.noOp import noOp
from azioni.mossaAsincrona import mossaAsincrona
from azioni.mossaSincrona import mossaSincrona

from agenteMossaAsincrona import agenteMossaAsincrona

from threading import Thread


class Attaccante(Agente):
    def __init__(self):
        super().__init__()
        self.sincronaAzione = mossaSincrona()
        self.asincronaAzione = mossaAsincrona()

        self.REWARD_MAP = {
            0 : (1,1,1),
            1 : (1,1,1),
        }


    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves,mosse):     
        mAttS = mosse['attaccante']['sincrone']
        mAttA = mosse['attaccante']['asincrone']

        super().preCondizioni(spazio,legal_moves,mAttS,mAttA)


    def postCondizioni(self,action,spazio,agent,mosse,timer):
        mAttS = mosse['attaccante']['sincrone']
        mAttA = mosse['attaccante']['asincrone']

        #-----------------------------------------------------
        # tempo appicazione della mossa sincrona
        t = 0
        # nuovo agente asincrono
        agente = 0
        # tempo mossa difensore turno precedente
        delta = abs(spazio[agent][timer]-self.lastTimer)
        # azzero i nop
        #spazio[agent][22] = 0
        #-----------------------------------------------------

        # esempio prima mosse sincrone 0-9 (10) e poi 10-14 asincrone (5): 15 mosse tot 10 e 5 
        if action < mAttS :
            self.sincronaAzione.postCondizione(spazio,agent,action)
            t = 0.5
        else:
            agente = agenteMossaAsincrona(self.asincronaAzione,action,spazio,agent)
         
        spazio[agent][timer] -= round(t,2)
        
        #----------------------------------------------------------------------------
        self.aggiornaMosseAsincrone(round(delta+t,2),agente,action)

        self.lastTimer = round(spazio[agent][timer],2)
        #----------------------------------------------------------------------------

        
    def reset(self):
        super().reset()
        self.asincronaAzione.reset()
        self.sincronaAzione.reset()

        self.mosseAsincroneRunning = []
        