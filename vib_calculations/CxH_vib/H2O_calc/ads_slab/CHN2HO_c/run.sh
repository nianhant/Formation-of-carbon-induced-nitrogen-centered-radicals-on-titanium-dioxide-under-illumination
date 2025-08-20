#!/bin/bash
#PBS -N CxH_vib/CHN2HO_c
#PBS -l nodes=1:ppn=8,pmem=8gb
#PBS -l walltime=72:00:00
#PBS -o stdout
#PBS -e stderr
#PBS -m abe
#PBS -A GT-amedford6-joe
#PBS -M ntian30@gatech.edu
cd $PBS_O_WORKDIR
source ~/.bashrc
source /storage/coda1/p-amedford6/0/shared/rich_project_chbe-medford/medford-share/envs/espresso-6.7MaX-beef-ipi_nianhant
setpseudos espresso_nninc_pbe_van
python run.py