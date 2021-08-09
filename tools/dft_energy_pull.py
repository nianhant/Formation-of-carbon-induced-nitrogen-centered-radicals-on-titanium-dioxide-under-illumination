import os
from ase.io import read
import numpy as np
from ase.thermochemistry import *

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def slab_eng(path):
    cur_dir = os.path.realpath(path+'/slab')
    slab = {}
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'energy.txt' in files:
            result = float(readFile(root + '/energy.txt')[0])
            name = root.split('/')
            sur = name[-1]
            slab[sur] = result
    return slab

def ads_slab_eng(path):
    cur_dir = os.path.realpath(path+'/ads_slab')
    ads_slab = dict()
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'energy.txt' in files:
            result = float(readFile(root + '/energy.txt')[0])
            name = root.split('/')
            adsorbate_order = name[-1]
            adsorbate = adsorbate_order.split('_')[-2]
            order = adsorbate_order.split('_')[-1]
            if adsorbate not in ads_slab:
                ads_slab[adsorbate] = {}
            ads_slab[adsorbate][order] = result
    return ads_slab

# Return a dictionary of existing reference energy
def reference_eng(path):
    ads_slab = ads_slab_eng(path)
    reference = dict() 
    cur_dir = os.path.realpath(path + '/reference')
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'energy.txt' in files:
            result = float(readFile(root + '/energy.txt')[0])
            name = root.split('/')
            ads = name[-1]
            reference[ads] = result
    return reference 









