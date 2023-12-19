from Agente import Agente
from azioni.GenerateAlert import GenerateAlert 
from azioni.FirewallActivation import FirewallActivation
from azioni.BlockIp import BlockIp 
from azioni.UnBlockIp import UnBlockIp
from azioni.LimitFlowRate import LimitFlowRate
from azioni.UnLimitFlowRate import UnLimitFlowRate
from azioni.RedirectHoneypot import RedirectHoneypot
from azioni.UnRedirectHoneypot import UnRedirectHoneypot
from azioni.IncreaseLog import IncreaseLog
from azioni.DecreaseLog import DecreaseLog
from azioni.Quarantine import Quarantine
from azioni.UnQuarantine import UnQuarantine
from azioni.ManualResolution import ManualResolution
from azioni.Reboot import Reboot
from azioni.ShutDown import ShutDown
from azioni.Start import Start
from azioni.Backup import Backup
from azioni.Update import Update
from azioni.noOp import noOp
from azioni.mossaAsincrona import mossaAsincrona
from azioni.mossaSincrona import mossaSincrona

from threading import Thread
from agenteMossaAsincrona import agenteMossaAsincrona

import random


class Difensore(Agente):
    def __init__(self):
        super().__init__()
        self.sincronaAzione = mossaSincrona()
        self.asincronaAzione = mossaAsincrona()

        self.REWARD_MAP = {
            0 : (1,1,1),
            1 : (1,1,1),
        }

    # Il difensore invece può eseguire una mossa solo nel caso incui il Timer è <=0 ed ogni mossa vale 1
    def preCondizioni(self,spazio,legal_moves,mosse,agent):
        
        mAttS = mosse[agent]['sincrone']
        mAttA = mosse[agent]['asincrone']

        super().preCondizioni(spazio,legal_moves,mAttS,mAttA,agent)
        



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
        
        spazio[agent][timer] += round(t,2)
        
        #----------------------------------------------------------------------------
        self.aggiornaMosseAsincrone(round(delta+t,2),agente,action)

        self.lastTimer = round(spazio[agent][timer],2)
        #----------------------------------------------------------------------------

    
    
    def reset(self):
        super().reset()
        self.asincronaAzione.reset()
        self.sincronaAzione.reset()

        self.mosseAsincroneRunning = []