# IRS: Intrusion Response System

INSTALLARE
requirements.txt

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

