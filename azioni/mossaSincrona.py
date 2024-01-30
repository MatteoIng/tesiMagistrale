import random

# Nel paper abbiamo che l'attaccante incrementa un contatore con una probabilità di 0.05 (5%??)
# il difensore lo decrementa con una probabilita di 1/10 (10%?)
# ogni azione sincrona corrisponde una componente nello spazio
# l'attaccante riesce nell'attacco con una probabilità pari al 5%
# il difensore al 10%

class mossaSincrona():
    
    def preCondizione(self,spazio,legal_moves,mAttS,agent,mosseEseguite):
        print('MOSSE GIA ESEGUITE:',mosseEseguite)
    
        if agent == 'attaccante':
            # scorro mosse sinc...
            for i in range(mAttS):
                # mossa sinc mai eseguita...
                if (i not in mosseEseguite):
                    # classiche pre consizioni...
                    for j in range(i+1):
                        if spazio['difensore'][j] == 0 :
                            legal_moves[i] = 1
                            break
                        else:
                            legal_moves[i] = 0
                # mossa sinc già eseguita...
                else:
                    legal_moves[i] = 0
        else:
            # scorro mosse sinc...
            for i in range(mAttS):
                # mossa sinc mai eseguita...
                if (i not in mosseEseguite):
                    # classiche pre consizioni...
                    for j in range(i+1):
                        if spazio[agent][j] == 1 :
                            legal_moves[i] = 1
                            break
                        else:
                            legal_moves[i] = 0
                # mossa sinc già eseguita...
                else:
                    legal_moves[i] = 0
                
    
    def postCondizione(self,spazio,agent,action):
        
        #soglia = round(random.random(),2)

        if agent == 'attaccante':
                for i in range(action+1):
                    # probabilità per ogni mossa
                    #prob = round(random.random(),2)
                    #if prob <= soglia :
                    spazio['difensore'][i] = 1
        else:    
            for i in range(action+1):
                    # probabilità per ogni mossa
                    #prob = round(random.random(),2)
                    #if prob <= soglia :
                    spazio['difensore'][i] = 0
        


