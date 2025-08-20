import os
# import pathlib
from shutil import copy, move
from time import time


def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def time_per_SCF(path):
    sparc_out = readFile(path)
    valid_output = []
    for i,line in enumerate(sparc_out):
        if 'Start time' in line:
            # print(i)
            valid_output=sparc_out[i:]

    # print(valid_output)
    for i,line in enumerate(valid_output):
        if 'No.1 Exx outer loop:' in line:
            scf_results =valid_output[i:]
            # print(i)
            break

    n_SCF = 0
    for i,line in enumerate(scf_results):
        if 'Total number of SCF:' in line:
            # print(line)
            item_list = line.split(' ')
            n_cycle = item_list[4]
            n_SCF+=int(n_cycle)
    # print(scf_results)
    scf_index=[[],[]]
    for i,line in enumerate(valid_output):
        if 'No.' in line:
            scf_index[0].append(i)
            for j,line in enumerate(valid_output[i:]):
                if 'Total number of SCF:' in line:
                    scf_index[1].append(j+i)
                    break
    # print(scf_index)
    tot_time = 0
    for x in range(len(scf_index[0])):
        i = scf_index[0][x]
        j=scf_index[1][x]
        time_list = valid_output[i+1:j]
        for item in time_list:
            time = item.split('\n')[0]
            time = time.split(' ')[-1]
            time=float(time)
            tot_time += time
    # print(tot_time/n_SCF)
    return tot_time/n_SCF
            

path_list =['441_downsample/ads_slab/CH3N_a/sprc-calc.out',
            '441_downsample/slab/rutile_O_br_vacant/sprc-calc.out',
            '441/ads_slab/CH3N_a/sprc-calc.out',
            '441/slab/rutile_O_br_vacant/sprc-calc.out',
            '../HSE_ads/ads_slab/CH3N_a/sprc-calc.out',
            '../HSE_slab/slab/rutile_O_br_vacant/sprc-calc.out']

for path in path_list:
    print(path, time_per_SCF(path))