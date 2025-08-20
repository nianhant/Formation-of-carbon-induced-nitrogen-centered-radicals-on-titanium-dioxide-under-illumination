#!/bin/bash
#PBS -N ads_slab/CHN2_b
#PBS -l nodes=1:ppn=6:gpus=1:RTX6000,mem=128gb
#PBS -l walltime=24:00:00
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