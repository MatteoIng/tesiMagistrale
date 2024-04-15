# IRS: Intrusion Response System
# Solo difensore

INSTALLARE
requirements.txt

NON MODIFICARE NUMERO GIOCATORI (non implementato ancora)


COMANDI:
 ./start.sh ALGORITMO TrainingIteration Gamma
 ./start.sh ALGORITMO -e CheckPoint
 ./start.sh ALGORITMO TrainingIteration Gamma rangeCpusFisiche

LEGENDA:
 - ALGORITMI: DQN, ApexDQN, Impala, PG, PPO
 - TrainingIteration: int

in c220g5 ho 2 socket (processori fisici), con 10 core ognuno, ognuno 2 thread
ovvero 40 processori logici, il range sarà: 0-9 primo processore, 10-19 secondo
oppure 0-1,10-11 per usare i primi due core di entrambi


OUTPUT
/fileGrafici/reward_mosse.txt

VISUALIZZAZIONE
Tutte le visualizzazione differenti e custom sono nell'altra repository: /visualizzazioniCustom (UTILIZZATI PER I TEST SU MACCHINE REMOTE UNA VOLTA SCARICATI I FILE IN LOCALE)

./visualizzazione.py (UTILIZZATO PER TEST SUL PC PERSONALE PER RISCONTRO GRAFICO)
/fileGrafici/visualizzaAll.py (NON UTILIZZATO)

./caricamentoserver.SH
Ci sono tutti i file indispensabili per la run, script per il caricamento automatizzato

./evaluate/*
file per l'evaluation dei checkpoint
