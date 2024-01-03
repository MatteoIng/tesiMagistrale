
class Agente():
    def __init__(self):
        self.T1 = 0.33
        self.T2 = 0.66

        self.mosseAsincroneRunning = []
        # Per le mosse asincrone, per il calcolo del tempo del difensore
        self.lastTimer = 0

        self.wt = 0.60
        self.wc = 0
        self.wi = 0.40
        self.tMax = 400
        self.cMax = 500

    def reward(self,azione):
        #  CONSIDERA SOLO IL TEMPO NELLA REWARD
        # CONSIDERARE COME CONTEGGIARE IL TEMPO E L'ASINCRONICITA
        # MINIMIZZARE IL TEMPO
        calcolo = -(-self.wt*(azione[0]/self.tMax)-self.wc*(azione[1]/self.cMax)-self.wi*azione[2])
        #calcolo = -(-self.wt*(azione[0]/self.tMax))
        print('Reward:',calcolo)
        return calcolo
    
    def reset(self):
        self.mosseAsincroneRunning = []

    def aggiornaMosseAsincrone(self,tot,agente,action):
        # Questo mi servirebbe a far scattare il tempo delle mosse asincrone
        # calcolo anche il delta della mossa del difensore + dell'attaccante
        print('Mosse Asincrone in Running PRIMA della mossa:',self.mosseAsincroneRunning)
        print('len:',len(self.mosseAsincroneRunning))

        # lA LISTA RIMOZIONI la utilizzo per rimuovere tutte quelle azioni asincrone che vengono eseguite
        # non le elimino direttmente perche togliendo elementi dalla lista mentre la eseguo smonto 
        # l'ordine degli elementi rispetto l'indice
        listaRimozioni = []
        for i in self.mosseAsincroneRunning:
            print(i)
            # richiama il metodo dell'agente asincrono per aggiornare il tempo sulla mossa ed eventualmente applicarla
            val = i[0].stepSuccessivo(tot)
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