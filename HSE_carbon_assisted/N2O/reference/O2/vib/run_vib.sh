#!/bin/bash
#PBS -l nodes=1:ppn=10
#PBS -l walltime=12:00:00
#PBS -q joe
#PBS -N O2
#PBS -o stdout
#PBS -e stderr
cd $PBS_O_WORKDIR

source  /gpfs/pace1/project/chbe-medford/medford-share/envs/espresso-5.1.r11289-pybeef

python vib_calc.py #submit using mpirun (parallel computing) to 12 cores. The 12 here must match the ppn specified in the header.
