from Agente import Agente


class Attaccante(Agente):

    def __init__(self):
        super().__init__()


    # Se l'attaccante trova il Timer <=0 non puo eseguire e per ora facciamo che ogni azione vale 1
    def preCondizioni(self,spazio,legal_moves,mosse,agent,timer):     
        mAttS = mosse[agent]['sincrone']
        mAttA = mosse[agent]['asincrone']

        return super().preCondizioni(spazio,legal_moves,mAttS,mAttA,agent,timer)
            
    
    def postCondizioni(self,action,spazio,agent,mosse,timer):
        mAttS = mosse['attaccante']['sincrone']
        mAttA = mosse['attaccante']['asincrone']
        mAttT = mAttS+mAttA

        return super().postCondizioni(action,spazio,agent,mosse,timer,mAttS)
    

    def reward(self, azione,n_azioni):
        return (azione - (n_azioni-2))/ (n_azioni-2)


    def reset(self):
        super().reset()
        self.asincronaAzione.reset()
        #self.sincronaAzione.reset()
        