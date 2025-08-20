#!/bin/bash
#PBS -N BEEF_carbon_assisted/CH2N2H_a
#PBS -l nodes=1:ppn=6,pmem=16gb
#PBS -l walltime=72:00:00
#PBS -o stdout
#PBS -e stderr
#PBS -m abe
#PBS -A GT-amedford6-joe
#PBS -M ntian30@gatech.edu
cd $PBS_O_WORKDIR
source ~/.bashrc
source /storage/coda1/p-amedford6/0/shared/rich_project_chbe-medford/medford-share/envs/espresso-7.0
setpseudos espresso_nninc_pbe_van
python run.py