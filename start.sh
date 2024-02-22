#!/bin/bash

if [ "$1" = "-h" ]; then
	echo 'COMANDI:'
	echo ' ./start.sh ALGORITMO TrainingIteration Gamma'
	echo ' ./start.sh ALGORITMO -e CheckPoint'
	echo ' ./start.sh ALGORITMO TrainingIteration Gamma rangeCpusFisiche'
	echo ''
	echo 'LEGENDA:'
	echo ' - ALGORITMI: DQN, ApexDQN, Impala, PG, PPO'
	echo ' - TrainingIteration: int'
	echo 'in c220g5 ho 2 socket (processori fisici), con 10 core ognuno, ognuno 2 thread'
	echo 'ovvero 40 processori logici, il range sarà: 0-9 primo processore, 10-19 secondo'
	echo 'oppure 0-1,10-11 per usare i primi due core di entrambi'
fi

if [ "$2" = "-e" ]; then
	if [ "$1" = "PG" ]; then
		clear && python3 ./evaluate/evaluationPG.py $3 > log.txt
	fi
	if [ "$1" = "PPO" ]; then
		clear && python3 ./evaluate/evaluationPPO.py $3 > log.txt
	fi
	if [ "$1" = "DQN" ]; then
		clear && python3 ./evaluate/evaluationDQN.py $3 > log.txt
	fi
	if [ "$1" = "ApexDQN" ]; then
		clear && python3 ./evaluate/evaluationApexDQN.py $3 > log.txt
	fi
	if [ "$1" = "Impala" ]; then
		clear && python3 ./evaluate/evaluationImpala.py $3 > log.txt
	fi
else
	if [ "$1" = "PG" ]; then
		if [ "$4" != "" ]; then
			clear && taskset -c $4 python3 ./training/run_rspPG.py $2 $3
		else
			clear && python3 ./training/run_rspPG.py $2 $3
		fi
	fi
	if [ "$1" = "PPO" ]; then
		if [ "$4" != "" ]; then
			clear && taskset -c $4 python3 ./training/run_rspPPO.py $2 $3
		else
			clear && python3 ./training/run_rspPPO.py $2 $3
		fi
	fi
	if [ "$1" = "DQN" ]; then
		if [ "$4" != "" ]; then
			clear && taskset -c $4 python3 ./training/run_rspDQN.py $2 $3
		else
			clear && python3 ./training/run_rspDQN.py $2 $3
		fi
	fi
	if [ "$1" = "ApexDQN" ]; then
		if [ "$4" != "" ]; then
			clear && taskset -c $4 python3 ./training/run_rspApexDQN.py $2 $3
		else
			clear && python3 ./training/run_rspApexDQN.py $2 $3
		fi
	fi
	if [ "$1" = "Impala" ]; then
		if [ "$4" != "" ]; then
			clear && taskset -c $4 python3 ./training/run_rspImpala.py $2 $3
		else
			clear && python3 ./training/run_rspImpala.py $2 $3
		fi
	fi
fi 

