#!/bin/bash
#PBS -N NH3
#PBS -l nodes=12:ppn=24
#PBS -l pmem=10GB
#PBS -l walltime=10:00:00
#PBS -o stdout
#PBS -e stderr
#PBS -m abe
#PBS -A GT-amedford6-joe

source ~/.bashrc
cd $PBS_O_WORKDIR
source /storage/coda1/p-amedford6/0/shared/rich_project_chbe-medford/medford-share/envs/dev_SPARC_10_08_2021

python run.py
