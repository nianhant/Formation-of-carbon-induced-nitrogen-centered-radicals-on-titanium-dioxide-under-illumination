import os
import pickle
from shutil import copy, move
import numpy as np
from ase.symbols import string2symbols

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def ads_slab_eng(path):
    cur_dir = os.path.realpath(path)
    eng_dict=dict()
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'ensemble_np.txt' in files:
            result = [float(i) for i in readFile(root + '/ensemble_np.txt')]
            name = root.split('/')
            if 'reference' in path or 'slab' in path:
                adsorbate = name[-1]
            else:
                adsorbate_order = name[-1]
                adsorbate = adsorbate_order.split('_')[-2]
                # order = adsorbate_order.split('_')[-1]
            eng_dict[adsorbate] = np.array(result)
    return eng_dict

# CH_dict = ads_slab_eng('CH_BEEF')
# CH2_dict = ads_slab_eng('CH2_BEEF')
CH3_dict = ads_slab_eng('CH3_BEEF')
# print(CH3_dict['CH3N2'])
print(CH3_dict['Ben'].mean())
print(CH3_dict['CH3'].mean())

# ref_dict = ads_slab_eng('reference_BEEF')
# slab_dict = ads_slab_eng('slab_BEEF')

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


num_bins = 100
# n, bins, patches = plt.hist(CH3_dict['Ben'], num_bins, facecolor='blue', alpha=0.5)
# # plt.show()
# plt.savefig('Ben.png')

n, bins, patches = plt.hist(CH3_dict['CH3'], num_bins, facecolor='blue', alpha=0.5)
plt.savefig('CH3.png')
