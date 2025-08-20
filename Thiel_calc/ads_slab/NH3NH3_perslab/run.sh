#!/bin/bash
#PBS -N Thiel_calc/NH3NH3_perslab
#PBS -l nodes=1:ppn=4,pmem=10
#PBS -l walltime=72:00:00
#PBS -o stdout
#PBS -e stderr
#PBS -m abe
#PBS -A GT-amedford6-joe
#PBS -M ntian30@gatech.edu
cd $PBS_O_WORKDIR
source ~/.bashrc
source /storage/coda1/p-amedford6/0/shared/rich_project_chbe-medford/medford-share/envs/espresso-6.8

setpseudos espresso_nninc_pbe_van
python run.py