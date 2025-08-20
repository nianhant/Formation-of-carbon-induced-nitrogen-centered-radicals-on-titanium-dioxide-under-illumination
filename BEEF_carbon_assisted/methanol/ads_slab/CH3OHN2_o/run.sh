#!/bin/bash
#PBS -N ads_slab/CH3OHN2_o
#PBS -l nodes=1:ppn=8,pmem=18
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