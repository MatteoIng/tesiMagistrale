
class Agente():
    def __init__(self):
        self.T1 = 0.33
        self.T2 = 0.66

        self.mosseAsincroneRunning = []
        # Per le mosse asincrone, per il calcolo del tempo del difensore
        #self.lastTimer = 0
        self.mosseEseguite = []

        self.wt = 1
        self.wc = 0
        self.wi = 0
        self.tMax = 1
        self.cMax = 1

    def lenMosseEseguite(self):
        return len(self.mosseEseguite)

    def preCondizioni(self,spazio,legal_moves,mAttS,mAttA,agent,timer):
        mAttT = (mAttS+mAttA)

        if (spazio['difensore'][timer] <=0 and agent == 'difensore'):
            # Per tutte le mosse sincrone
            self.sincronaAzione.preCondizione(spazio,legal_moves,mAttS,agent,self.mosseEseguite)

            # Per tutte le mosse asincrone
            for mossa in range(mAttS,mAttT,1):
                if not(any(tupla[1] == mossa for tupla in self.mosseAsincroneRunning)):
                    self.asincronaAzione.preCondizione(spazio,legal_moves,mossa,agent,mAttS,self.mosseEseguite)
                else:
                    legal_moves[mossa] = 0
        
        if (spazio['difensore'][timer] >=0 and agent == 'attaccante'):
            # Per tutte le mosse sincrone
            self.sincronaAzione.preCondizione(spazio,legal_moves,mAttS,agent,self.mosseEseguite)

            # Per tutte le mosse asincrone
            for mossa in range(mAttS,mAttT):
                #print(f'PRECONDIZIONI MOSSE ASINCRONE:{mossa}')
                # mossa asincrona non in running
                if not(any(tupla[1] == mossa for tupla in self.mosseAsincroneRunning)):
                    self.asincronaAzione.preCondizione(spazio,legal_moves,mossa,agent,mAttS,self.mosseEseguite)
                else:
                    legal_moves[mossa] = 0

        # controllo che nessuna mossa sia eseguibile 
        check = [ not(legal_moves[i]) for i in range(len(legal_moves)-1)]
        #print(f'CHECK NOOP:{check}')
        if all(check):
            # abilito la noop
            legal_moves[timer] = 1
        else:
            legal_moves[timer] = 0
        


    def reward(self,azione):
        #  CONSIDERA SOLO IL TEMPO NELLA REWARD
        # CONSIDERARE COME CONTEGGIARE IL TEMPO E L'ASINCRONICITA
        # MINIMIZZARE IL TEMPO
        # VEDERE ALTRE IDEE MA CONSIDERARE ANCHE L'INTRODUZIONE DELL NMOSSE O DEL TEMPO
        # calcolo = -(-self.wt*(azione[0]/self.tMax)-self.wc*(azione[1]/self.cMax)-self.wi*azione[2])
        calcolo = -(-self.wt*(azione[0]/self.tMax))
        #calcolo = azione[0]
        print('Reward:',calcolo)
        return calcolo
    
    def reset(self):
        self.mosseAsincroneRunning = []
        self.mosseEseguite = []

    def aggiornaMosseAsincrone(self,tot,agente,action,mAttS):
        # Questo mi servirebbe a far scattare il tempo delle mosse asincrone
        # calcolo anche il delta della mossa del difensore + dell'attaccante
        print('Mosse Asincrone in Running PRIMA della mossa:',self.mosseAsincroneRunning)    
        print('tot:',tot)
        
        # lA LISTA RIMOZIONI la utilizzo per rimuovere tutte quelle azioni asincrone che vengono eseguite
        # non le elimino direttmente perche togliendo elementi dalla lista mentre la eseguo smonto 
        # l'ordine degli elementi rispetto l'indice
        listaRimozioni = []
        for i in self.mosseAsincroneRunning:
            print(i)
            print('Tempo Attesa:',i[0].mossa.tempoAttesa)
            print('Tempo Attuazione:',i[0].mossa.tempoAttuazione)
            # richiama il metodo dell'agente asincrono per aggiornare il tempo sulla mossa ed eventualmente applicarla
            val = i[0].stepSuccessivo(tot,i[1],mAttS)
            if val :
                listaRimozioni.append(i)

        # rimuovo azoni asincrone eseguite
        for i in listaRimozioni:
            i[0].mossa.tempoAttesa = i[0].mossa.tempoAttuazione
            self.mosseAsincroneRunning.remove(i)
        listaRimozioni = []


        #La metto qui perche altrimenti anche quelle appena create mi subiscono il delta del difensore
        # del turno prima
        if agente != 0:
            self.mosseAsincroneRunning.append((agente,action))

        print('Mosse Asincrone in Running DOPO la mossa:',self.mosseAsincroneRunning)
        for i in self.mosseAsincroneRunning:
            print('Tempo Attesa:',i[0].mossa.tempoAttesa)
            print('Tempo Attuazione:',i[0].mossa.tempoAttuazione)