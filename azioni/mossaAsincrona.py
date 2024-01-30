import random

# qui ho implementato la stessa idea delle mosse sincrone

class mossaAsincrona():

    def __init__(self):
        self.tempoAttuazione = 1.0
        self.tempoAttesa = 1.0


    def preCondizione(self,spazio,legal_moves,pos,agent,mAttS,mosseEseguite,running):
        
        # mossa asincrona non in esecuzione...
        if not(running):
            if agent == 'attaccante':
                # mossa asincrona mai eseguita...
                if (pos not in mosseEseguite):
                    #for i in range(mAttS,len(legal_moves)):
                    # classica pre condizione di abilitazione...
                    for j in range(pos+1):
                        #print(f'pos {pos} j {j}')
                        if spazio['difensore'][j] == 0 :
                            #print(f'LEGAL PRIMA {legal_moves}')
                            legal_moves[pos] = 1
                            #print(f'LEGAL DOPO {legal_moves}')
                            break
                        else:
                            legal_moves[pos] = 0
                # mossa asinc giaà eseguita...
                else:
                    legal_moves[pos] = 0
            else:
                # mossa asincrona mai eseguita...
                if (pos not in mosseEseguite):
                    #for i in range(mAttS,len(legal_moves)):
                    # classica pre condizione di abilitazione...
                    for j in range(pos+1):
                        #print(f'pos {pos} j {j}')
                        if spazio['difensore'][j] == 1 :
                            #print(f'LEGAL PRIMA {legal_moves}')
                            legal_moves[pos] = 1
                            #print(f'LEGAL DOPO {legal_moves}')
                            break
                        else:
                            legal_moves[pos] = 0
                # mossa asinc giaà eseguita...
                else:
                    legal_moves[pos] = 0

        # mossa asincrona in esecuzione
        else:
            legal_moves[pos] = 0


    def postCondizione(self,spazio,agent,action,mAttS):
        #soglia = round(random.random(),2)

        if agent == 'attaccante':
            #prob = round(random.random(),2)
            #if prob <= soglia :
            for i in range((action+1)):
                spazio['difensore'][i] = 1
        else:    
            #prob = round(random.random(),2)
            #if prob <= soglia :
            for i in range((action+1)):
                spazio['difensore'][i] = 0
        
    def reset(self):
        self.tempoAttesa = self.tempoAttuazione