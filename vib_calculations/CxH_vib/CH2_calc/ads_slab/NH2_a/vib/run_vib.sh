#!/bin/bash
#PBS -l nodes=1:ppn=14
#PBS -l walltime=48:00:00
#PBS -q joe
#PBS -N vib_NH2_d_4_layer
#PBS -o stdout
#PBS -e stderr
cd $PBS_O_WORKDIR

source  /gpfs/pace1/project/chbe-medford/medford-share/envs/espresso-5.1.r11289-pybeef_ase3.14_cust_esp

python vib_calc.py #submit using mpirun (parallel computing) to 12 cores. The 12 here must match the ppn specified in the header.
