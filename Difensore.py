from Agente import Agente

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
    def preCondizioni(self,spazio,legal_moves,mosse,agent,timer):
        
        mDiffS = mosse[agent]['sincrone']
        mDiffA = mosse[agent]['asincrone']
        super().preCondizioni(spazio,legal_moves,mDiffS,mDiffA,agent,timer)
        



    def postCondizioni(self,action,spazio,agent,mosse,timer,lastTimer):
        mDiffS = mosse['attaccante']['sincrone']
        mDiffA = mosse['attaccante']['asincrone']
        mDiffT = mDiffS+mDiffA

        #-----------------------------------------------------
        # tempo appicazione della mossa sincrona
        t = 0
        # nuovo agente asincrono
        agente = 0
        # tempo mossa difensore turno precedente
        #delta = abs(spazio[agent][timer]-self.lastTimer)
        #delta = lastTimer
        # azzero i nop
        #spazio[agent][22] = 0
        #-----------------------------------------------------

        # tnop usato perche nop non scala il tempo se l'agente ha ancora mosse asincrone e/o sincrone da fare
        # lo scala solo nel momento in cui il nop viene selezionato perche son finite le mosse
        # e devo scalare il tempo alle mosse asincrone affinche finiscano
        # ma non mi altera ai il timer
        tnop = 0
        # se l'azione è sincrona fa...
        if action < mDiffS :
            self.sincronaAzione.postCondizione(spazio,agent,action)
            self.mosseEseguite.append(action)
            t = 0.5
        # se l'azione è asincrona fa..
        else:
            if action != timer:
                agente = agenteMossaAsincrona(mossaAsincrona(),action,spazio,agent)
                agente.mossa.tempoAttesa = agente.mossa.tempoAttuazione
            else:
                # se invece la mossa è noop...
                # ed è i suo turno MA QUESTO IF FUNZIONA SOLO SE HANNO LO STESSO NUMERO DI AZIONI SINCRONE
                # PERCHE IL TIMER ALLA FINE SARà SEMPRE 0
                if spazio[agent][timer] <= 0:
                    # se ci sono mosse asincrone noop me le deve far terminare
                    t = 0.5
                    # verifico che tutte le mosse sincrone (SCALA TEMPO) siano state usate
                    for i in range(mDiffS):
                        # se almeno 1 non usata t = 0
                        if i not in self.mosseEseguite:
                            t = 0
                            tnop = 1
                            break

        # se tnop è 1 vuol dire che è stata scelta nop e nop scala 0.5 alle mosse asincrone
        # per forza ha finito le mosse
        # ma non deve alterarmi il timer in alcun modo
        if tnop == 0:
            spazio[agent][timer] += round(t,2)
        
        #----------------------------------------------------------------------------
        self.aggiornaMosseAsincrone(round(t,2),agente,action,mDiffS)
        # perche lamossa noop col numero combacia alla posizione del timer

        #lastTimer = round(spazio[agent][timer],2)
        #----------------------------------------------------------------------------
        return t

    
    
    def reset(self):
        super().reset()
        self.asincronaAzione.reset()
        self.sincronaAzione.reset()