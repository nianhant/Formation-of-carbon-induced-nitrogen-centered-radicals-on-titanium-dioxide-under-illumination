#!/bin/bash
#PBS -N Thiel_calc/N2HH_perslab
#PBS -l nodes=14:ppn=24
#PBS -l pmem=10GB
#PBS -l walltime=200:00:00
#PBS -o stdout
#PBS -e stderr
#PBS -m abe
#PBS -A GT-amedford6-joe
#PBS -M ntian30@gatech.edu

source ~/.bashrc
cd $PBS_O_WORKDIR
source /storage/coda1/p-amedford6/0/shared/rich_project_chbe-medford/medford-share/envs/dev_SPARC_10_08_2021
​
python run.py