from Agente import Agente


class Difensore(Agente):

    def __init__(self):
        super().__init__()


    # Il difensore invece può eseguire una mossa solo nel caso incui il Timer è <=0 ed ogni mossa vale 1
    def preCondizioni(self,spazio,legal_moves,mosse,agent,timer):
        
        mDiffS = mosse[agent]['sincrone']
        mDiffA = mosse[agent]['asincrone']
        super().preCondizioni(spazio,legal_moves,mDiffS,mDiffA,agent,timer)
        

    def postCondizioni(self,action,spazio,agent,mosse,timer):
        mDiffS = mosse['attaccante']['sincrone']
        mDiffA = mosse['attaccante']['asincrone']
        mDiffT = mDiffS+mDiffA

        return super().postCondizioni(action,spazio,agent,mosse,timer,mDiffS)


    def reset(self):
        super().reset()
        self.asincronaAzione.reset()
        #self.sincronaAzione.reset()