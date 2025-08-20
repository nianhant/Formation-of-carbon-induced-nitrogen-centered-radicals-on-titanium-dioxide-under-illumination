#!/bin/bash
#PBS -N ./N2H4
#PBS -l nodes=1:ppn=1
#PBS -l pmem=3GB
#PBS -l walltime=12:00:00
#PBS -o stdout
#PBS -e stderr
#PBS -m abe
#PBS -A GT-amedford6-joe
#PBS -M ntian30@gatech.edu
cd $PBS_O_WORKDIR
source ~/.bashrc
source /storage/coda1/p-amedford6/0/shared/rich_project_chbe-medford/medford-share/envs/espresso-7.0

setpseudos espresso_sssp_prec_v1#1_nonrel
python run.py