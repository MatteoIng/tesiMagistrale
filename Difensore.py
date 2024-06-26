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
from azioni.Wait import Wait

from threading import Thread
from agenteMossaAsincrona import agenteMossaAsincrona

import random


class Difensore(Agente):
    def __init__(self):
        super().__init__()
        self.GenerateAlertAzione = GenerateAlert()
        self.FirewallActivationAzione = FirewallActivation()
        self.BlockIpAzione = BlockIp()
        self.UnBlockIpAzione = UnBlockIp()
        self.LimitFlowRateAzione = LimitFlowRate()
        self.UnLimitFlowRateAzione = UnLimitFlowRate()
        self.RedirectHoneypotAzione = RedirectHoneypot()
        self.UnRedirectHoneypotAzione = UnRedirectHoneypot()
        self.IncreaseLogAzione = IncreaseLog()
        self.DecreaseLogAzione = DecreaseLog()
        self.QuarantineAzione = Quarantine()
        self.UnQuarantineAzione = UnQuarantine()
        self.ManualResolutionAzione = ManualResolution()
        self.RebootAzione = Reboot()
        self.ShutDownAzione = ShutDown()
        self.StartAzione = Start()
        self.BackupAzione = Backup()
        self.UpdateAzione = Update()
        self.noOp = noOp()
        self.wait = Wait()

        self.REWARD_MAP = {
            0 : (1,1,0),
            1 : (2,1,0),
            2 : (1,3,0.3),
            3 : (1,3,0),
            4 : (3,1,0.2),
            5 : (3,1,0),
            6 : (3,3,0.1),
            7 : (3,3,0),
            8 : (2,1,0.05),
            9 : (1,1,0),
            10 : (5,5,1),
            11 : (5,5,0),
            12 : (3600,200,0),
            13 : (60,6,0.7),
            14 : (30,6,1),
            15 : (30,6,0),
            16 : (3600,10,0.1),
            17 : (600,300,0.1),
            18 : (3600,300,0.1),
            # voglio scoraggiare il difensore a non fare nulla così che faccia qualcosa per salvaguardare
            # Con il professore abbiamo detto che deve essere in modulo la piu grande reward tra i due 
            # ed io ho aggiunto un delta per evitare il calcolo preciso prendendo i coefficenti maggiori (x,y,z)
            # sarebbe come a dire -inf
            19 : (0,0,0)
        }

    # Il difensore invece può eseguire una mossa solo nel caso incui il Timer è <=0 ed ogni mossa vale 1
    def preCondizioni(self,spazio,legal_moves):
        
        # Generate alert
        self.GenerateAlertAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # FirewallActivation
        # preso dal paper
        self.FirewallActivationAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # BlockSourceIp
        # preso dal paper
        self.BlockIpAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # UnblockSourceIp
        self.UnBlockIpAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # FlowRateLimit
        # preso dal paper
        self.LimitFlowRateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # UnlimitFlowRate
        self.UnLimitFlowRateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # RedirectToHoneypot
        self.RedirectHoneypotAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # UnHoneypot
        self.UnRedirectHoneypotAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # IncreaseLog
        self.IncreaseLogAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # DecreaseLog
        self.DecreaseLogAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # QuarantineHost
        self.QuarantineAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
          
        # UnQuarantineHost
        self.UnQuarantineAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # ManualResolution 
        self.ManualResolutionAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # SystemReboot
        self.RebootAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # SystemShutdown
        self.ShutDownAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # SystemStart
        self.StartAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # BackupHost
        if not(any(tupla[1] == 16 for tupla in self.mosseAsincroneRunning)):
            self.BackupAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore',self.mosseAsincroneRunning)
        else:
            legal_moves[16] = 0
        
        # SoftwareUpdate
        # detto dal prof: deve aver fatto backup
        self.UpdateAzione.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        
        # WAIT mi serve per le mosse asincrone per aspettare il tempo di completamento senza fare altro
        if len(self.mosseAsincroneRunning) >= 1:
            self.wait.preCondizione(spazio,legal_moves,self.T1,self.T2,'difensore')
        else:
            legal_moves[19] = 0

        # noOp (altrimenti se nulla è selezionbile sceglie a caso)
        # Ora abbiamo deciso di renderla ammissibile ad ogni stato così che possa terminare anche 
        # quando non ho piu mosse che mi portano sullo stato target (finale)
        self.noOp.preCondizione(spazio,legal_moves,self.T1,self.T2,self.__class__.__name__)



    def postCondizioni(self,action,spazio,agent):
      
        #-----------------------------------------------------
        # tempo appicazione della mossa sincrona
        t = 0
        # nuovo agente asincrono
        agente = 0
        # tempo mossa difensore turno precedente
        delta = abs(spazio[agent][21]-self.lastTimer)
        # azzero i nop
        spazio[agent][22] = 0
        #-----------------------------------------------------

        # GenerateAlert
        if action == 0 :
            self.GenerateAlertAzione.postCondizione(spazio,agent)
            # Timer
            t = self.GenerateAlertAzione.reward[0]
        
        # FirewallActivation
        elif action == 1 :
            self.FirewallActivationAzione.postCondizione(spazio,agent)
            # Timer
            t = self.FirewallActivationAzione.reward[0]
        
        # BlockSourceIp
        elif action == 2 :
            self.BlockIpAzione.postCondizione(spazio,agent)
            # Timer
            t = self.BlockIpAzione.reward[0]
        
        # UnblockSourceIp
        elif action == 3 :
            self.UnBlockIpAzione.postCondizione(spazio,agent)
            # Timer
            t = self.UnBlockIpAzione.reward[0]
        
        # FlowRateLimit
        elif action == 4 :
            self.LimitFlowRateAzione.postCondizione(spazio,agent)
            # Timer
            t = self.LimitFlowRateAzione.reward[0]
        
        # UnlimitFlowRate
        elif action == 5 :
            self.UnLimitFlowRateAzione.postCondizione(spazio,agent)
            # Timer
            t = self.UnLimitFlowRateAzione.reward[0]
        
        # RedirectToHoneypot
        elif action == 6 :
            self.RedirectHoneypotAzione.postCondizione(spazio,agent)
            # Timer
            t = self.RedirectHoneypotAzione.reward[0]
        
        # UnHoneypot
        elif action == 7 :
            self.UnRedirectHoneypotAzione.postCondizione(spazio,agent)
            # Timer
            t = self.UnRedirectHoneypotAzione.reward[0]
        
        # IncreaseLog
        elif action == 8 :
            self.IncreaseLogAzione.postCondizione(spazio,agent)
            # Timer
            t = self.IncreaseLogAzione.reward[0]
        
        # DecreaseLog
        elif action == 9 :
            """ self.mosseAsincroneRunning.append(action)
            Thread(target=self.DecreaseLogAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            print('AVVIATO -LOG')
             """
            self.DecreaseLogAzione.postCondizione(spazio,agent)
            # Timer
            t = self.DecreaseLogAzione.reward[0]
        
        # QuarantineHost
        elif action == 10 :
            self.QuarantineAzione.postCondizione(spazio,agent)
            # Timer
            t = self.QuarantineAzione.reward[0]
        
        # UnQuarantineHost
        elif action == 11 :
            self.UnQuarantineAzione.postCondizione(spazio,agent)
            # Timer
            t = self.UnQuarantineAzione.reward[0]
        
        # ManualResolution
        elif action == 12 :
            self.ManualResolutionAzione.postCondizione(spazio,agent)
            # Timer
            t = self.ManualResolutionAzione.reward[0]
        
        # SystemReboot
        elif action == 13 :
            self.RebootAzione.postCondizione(spazio,agent)
            # Timer
            t = self.RebootAzione.reward[0]
        
        # SystemShutdown
        elif action == 14 :
            self.ShutDownAzione.postCondizione(spazio,agent)
            # Timer
            t = self.ShutDownAzione.reward[0]
        
        # SystemStart
        elif action == 15 :
            self.StartAzione.postCondizione(spazio,agent)
            # Timer
            t = self.StartAzione.reward[0]
        
        # BackupHost
        elif action == 16 :
            #self.mosseAsincroneRunning.append(action)
            #Thread(target=self.BackupAzione.postCondizione,args=(spazio,agent,self.mosseAsincroneRunning,action)).start()
            agente = agenteMossaAsincrona(self.BackupAzione,action,spazio,agent)
            print('AVVIO BACKUP')
            # Timer
            #t = 0.1

        # SoftwareUpdate
        elif action == 17 :
            self.UpdateAzione.postCondizione(spazio,agent)
            # Timer
            t = self.UpdateAzione.reward[0]

        # Noop solo per il timer
        elif action == 18 :
            self.noOp.postCondizione(spazio,agent)
        
        # Wait
        elif action == 19 :
            self.wait.postCondizione(spazio,agent)
            t = self.mosseAsincroneRunning[0][0].mossa.tempoAttesa

        spazio[agent][21] += round(t,2)

        #----------------------------------------------------------------------------
        self.aggiornaMosseAsincrone(round(delta+t,2),agente,action)

        self.lastTimer = round(spazio[agent][21],2)
        #----------------------------------------------------------------------------

    def reward(self, action):
        azione = 0

        # GenerateAlert
        if action == 0 :
            azione = self.GenerateAlertAzione.reward
        
        # FirewallActivation
        elif action == 1 :
            azione = self.FirewallActivationAzione.reward
        
        # BlockSourceIp
        elif action == 2 :
            azione = self.BlockIpAzione.reward
        
        # UnblockSourceIp
        elif action == 3 :
            azione = self.UnBlockIpAzione.reward
        
        # FlowRateLimit
        elif action == 4 :
            azione = self.LimitFlowRateAzione.reward
        
        # UnlimitFlowRate
        elif action == 5 :
            azione = self.UnLimitFlowRateAzione.reward
        
        # RedirectToHoneypot
        elif action == 6 :
            azione = self.RedirectHoneypotAzione.reward
        
        # UnHoneypot
        elif action == 7 :
            azione = self.UnRedirectHoneypotAzione.reward
        
        # IncreaseLog
        elif action == 8 :
            azione = self.IncreaseLogAzione.reward
        
        # DecreaseLog
        elif action == 9 :
            azione = self.DecreaseLogAzione.reward
        
        # QuarantineHost
        elif action == 10 :
            azione = self.QuarantineAzione.reward
        
        # UnQuarantineHost
        elif action == 11 :
            azione = self.UnQuarantineAzione.reward
        
        # ManualResolution
        elif action == 12 :
            azione = self.ManualResolutionAzione.reward
        
        # SystemReboot
        elif action == 13 :
            azione = self.RebootAzione.reward
        
        # SystemShutdown
        elif action == 14 :
            azione = self.ShutDownAzione.reward
        
        # SystemStart
        elif action == 15 :
            azione = self.StartAzione.reward
        
        # BackupHost
        elif action == 16 :
            azione = self.BackupAzione.reward
        
        # SoftwareUpdate
        elif action == 17 :
            azione = self.UpdateAzione.reward

        # Noop solo per il timer
        elif action == 18 :
            azione = self.noOp.rewardDiff

        elif action == 19 : 
            azione = self.wait.reward

        return super().reward(azione)
    
    def reset(self):
        super().reset()
        self.GenerateAlertAzione.reset()
        self.FirewallActivationAzione.reset()
        self.BlockIpAzione.reset()
        self.UnBlockIpAzione.reset()
        self.LimitFlowRateAzione
        self.UnLimitFlowRateAzione.reset()
        self.RedirectHoneypotAzione.reset()
        self.UnRedirectHoneypotAzione.reset()
        self.IncreaseLogAzione.reset()
        self.DecreaseLogAzione.reset()
        self.QuarantineAzione.reset()
        self.UnQuarantineAzione.reset()
        self.ManualResolutionAzione.reset()
        self.RebootAzione.reset()
        self.ShutDownAzione.reset()
        self.StartAzione.reset()
        self.BackupAzione.reset()
        self.UpdateAzione.reset()

        self.mosseAsincroneRunning = []