#!/bin/bash

if [ "$1" = "-h" ]; then
	echo 'COMANDI:'
	echo ' ./start ALGORITMO TrainingIteration'
	echo ' ./start ALGORITMO -e CheckPoint'
	echo ''
	echo 'LEGENDA:'
	echo ' - ALGORITMI: DQN, ApexDQN, Impala, PG, PPO'
	echo ' - TrainingIteration: int'
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
		clear && python3 ./training/run_rspPG.py $2 $3
	fi
	if [ "$1" = "PPO" ]; then
		clear && python3 ./training/run_rspPPO.py $2 $3
	fi
	if [ "$1" = "DQN" ]; then
		clear && python3 ./training/run_rspDQN.py $2 $3
	fi
	if [ "$1" = "ApexDQN" ]; then
		clear && python3 ./training/run_rspApexDQN.py $2 $3
	fi
	if [ "$1" = "Impala" ]; then
		clear && python3 ./training/run_rspImpala.py $2 $3
	fi
fi 

