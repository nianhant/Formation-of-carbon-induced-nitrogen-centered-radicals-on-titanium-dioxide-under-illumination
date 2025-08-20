import os
from shutil import copy, move
import numpy as np
import matplotlib.pyplot as plt
# TOL_FOCK=5e-05, h = 0.075, KPOINT_GRID = [4, 4, 1],
def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

cur_dir = os.getcwd()
def get_eng_matrix(cur_dir):
    range_param_list = []
    eng_list = []
    eng_dict = {}
    for child in os.listdir(cur_dir):
        path = os.path.join(cur_dir, child)
        # print(path)
        if os.path.isdir(path):
            range_param = child.split('_')[-1]
            eng = readFile(path+'/HSE_energy.txt')[0]
            eng_dict[range_param]=float(eng)
    return eng_dict
N2_rutile_110 = 'ads_slab/N2_rutile_110_copy'
slab = 'slab/rutile_O_br_vacant_copy'
N2 = 'reference/N2_copy'
N2_rutile_110_eng=get_eng_matrix(N2_rutile_110)
slab_eng = get_eng_matrix(slab)
N2_eng=get_eng_matrix(N2)

ads_eng={}
for key in N2_rutile_110_eng:
    ads_eng[key] = N2_rutile_110_eng[key] - N2_eng[key] - slab_eng[key]
print(ads_eng)
# print(N2_rutile_110_eng)
# print(slab_eng)
# print(N2_eng)

