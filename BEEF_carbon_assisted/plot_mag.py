import os
import matplotlib.pylab as plt

from subprocess import call
import sys
import json
from shutil import copy, move
import re
import pickle

def pickle_load_vib(file_name):
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    return b

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

# BEEF_mag = pickle_load_vib('BEEF_carbon_mag.pkl')
# HSE_mag = pickle_load_vib('HSE_carbon_mag.pkl')
BEEF_spin_pol_binding = pickle_load_vib('BEEF_carbon_assisted_binding.pkl')
BEEF_spin_paired_binding = pickle_load_vib('BEEF_spin_paired_binding.pkl')

BEEF_spin_pol_binding.pop('N2_rutile_110')
BEEF_spin_pol_binding.pop('CN2')
BEEF_spin_paired_binding.pop('CN2')
BEEF_spin_paired_binding.pop('N2')
print(BEEF_spin_pol_binding)
new_BEEF_spin_pol_binding = {}
for key in BEEF_spin_pol_binding:
    ads = key.split('_')[0]
    if ads in BEEF_spin_paired_binding:
        if ads != 'N2' and ads !='CH2NH':
            new_BEEF_spin_pol_binding[ads] = BEEF_spin_pol_binding[key]

# print(new_BEEF_spin_pol_binding)
for i, legend in [(new_BEEF_spin_pol_binding, 'spin pol'),(BEEF_spin_paired_binding, 'spin paired')]:
    lists = sorted(i.items()) # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples
    l=[]
    # for i in x:
    #     if i !='N2':
    #         l.append(i)
    plt.scatter(x, y, label = legend)
    plt.xticks(rotation = 90)
plt.legend()
plt.savefig('mag_comparison.png', bbox_inches='tight')