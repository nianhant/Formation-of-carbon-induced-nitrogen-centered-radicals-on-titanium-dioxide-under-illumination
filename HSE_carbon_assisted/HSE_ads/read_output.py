import os
from shutil import copy, move
import numpy as np
import matplotlib.pyplot as plt

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

cur_dir = os.getcwd()
def get_eng_matrix(cur_dir):
    # for child in os.listdir(cur_dir):
    #     path = os.path.join(cur_dir, child)
    eng = float(readFile(cur_dir+'/HSE_energy.txt')[0])
    return eng
CH3N2 = 'ads_slab/CH3N2_c'
CH3= 'ads_slab/CH3_a'
N2_rutile_110 = 'ads_slab/N2_rutile_110'
slab = 'slab/rutile_O_br_vacant'
CH3OH = '../HSE_ref/reference/CH3OH'
N2 = '../HSE_ref/reference/N2'
O2 =  '../HSE_ref/reference/O2'
H2 = '../HSE_ref/reference/H2'
H2O = '../HSE_ref/reference/H2O'

CH3N2_eng = get_eng_matrix(CH3N2)
N2_rutile_110_eng = get_eng_matrix(N2_rutile_110)
CH3_eng = get_eng_matrix(CH3)
slab_eng = get_eng_matrix(slab)#[0]
CH3OH_eng = get_eng_matrix(CH3OH)#[0]

N2_eng = get_eng_matrix(N2)#[0]

H2_eng = get_eng_matrix(H2)#[0]

H2O_eng = get_eng_matrix(H2O)#[0]

H_eng = 0.5*H2_eng
O_eng = H2O_eng - H2_eng
C_eng = CH3OH_eng - O_eng - 4* H_eng

CH3_ref_eng = C_eng+H_eng*3
CH3_ads_eng = CH3_eng-CH3_ref_eng-slab_eng
print('CH3 adsorption energy: ', CH3_ads_eng)

# print('CH3N2_slab:','\n',CH3N2_eng)
# print('N2_slab:','\n',N2_rutile_110_eng)
# print('slab:','\n',slab_eng)

CH3N2_eng = CH3N2_eng - slab_eng - N2_eng - C_eng - 3*H_eng
print('CH3N2 adsorption energy: ',CH3N2_eng)

# N2_rutile_110_eng_matrix = N2_rutile_110_eng - slab_eng - N2_eng 
# print('N2 adsorption energy:', '\n',N2_rutile_110_eng_matrix)

# CH3N2_ref = -(- N2_eng - C_eng - 3*H_eng)
# print('CH3N2 calculated reference energy:', '\n',CH3N2_ref)

# # CH3N2_ref = -(- N2_eng - C_eng - 3*H_eng)
# print('N2 reference energy:', '\n',N2_eng)

# CH3N2_ads = float(readFile('ads_slab/CH3N2_c/HSE_energy.txt')[0])
# # N2_ads = float(readFile('ads_slab/CH3N2_c/f_5e-05_h_0.079_k_4/HSE_energy.txt')[0])
# SLAB = float(readFile('slab/rutile_O_br_vacant/HSE_energy.txt')[0])

# print(CH3N2_ads - SLAB - CH3N2_ref)

