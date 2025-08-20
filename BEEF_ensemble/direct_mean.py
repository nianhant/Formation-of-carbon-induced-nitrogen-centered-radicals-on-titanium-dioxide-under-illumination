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

CH_dict = ads_slab_eng('CH_BEEF')
CH2_dict = ads_slab_eng('CH2_BEEF')
CH3_dict = ads_slab_eng('CH3_BEEF')
# print(CH3_dict['Ben'])
ref_dict = ads_slab_eng('reference_BEEF')
slab_dict = ads_slab_eng('slab_BEEF')

ref_dict['H'] = 0.5*ref_dict['H2']
ref_dict['N'] = 0.5*ref_dict['N2']
ref_dict['O'] = ref_dict['H2O'] - ref_dict['H2']
ref_dict['C'] = ref_dict['CH3OH'] - 4*ref_dict['H'] - ref_dict['O']

ads_ensemble_dict = dict()
for en_dict in [CH_dict, CH2_dict, CH3_dict]:
    for k in en_dict.keys():
        # print(np.sum(en_dict[k]))
        ads_ensemble_dict[k]=dict()#=en_dict[k]
        # print(en_dict[k].mean())
        ads_ensemble_dict[k]['mean'] = en_dict[k].mean()
        ads_ensemble_dict[k]['std'] = en_dict[k].std()
        ads_ensemble_dict[k]['sum'] = np.sum(en_dict[k])
# print(ads_ensemble_dict)
ref_ensemble_dict = dict()
# for en_dict in [ref_formation_ensemble]:
for en_dict in [ref_dict]:
    for k in en_dict.keys():
        # print(np.sum(en_dict[k]))
        ref_ensemble_dict[k]=dict()#=en_dict[k]
        ref_ensemble_dict[k]['mean'] = en_dict[k].mean()
        ref_ensemble_dict[k]['std'] = en_dict[k].std()
        ref_ensemble_dict[k]['sum'] = np.sum(en_dict[k])

slb_ensemble_dict=dict()
for en_dict in [slab_dict]:
    for k in en_dict.keys():
        # print(np.sum(en_dict[k]))
        slb_ensemble_dict[k]=dict()
        slb_ensemble_dict[k]['mean'] = en_dict[k].mean()
        slb_ensemble_dict[k]['std'] = en_dict[k].std()
        slb_ensemble_dict[k]['sum'] = np.sum(en_dict[k])
# print(slb_ensemble_dict) 
ads = ads_ensemble_dict['CH3N2']['sum']
ref = 2*ref_ensemble_dict['N']['sum']+3*ref_ensemble_dict['H']['sum']+ref_ensemble_dict['C']['sum']
slb = slb_ensemble_dict['rutile_O_br_vacant']['sum']
# print(ads_ensemble_dict['CH3N2']['sum'])
# print(2*ref_ensemble_dict['N']['sum']+3*ref_ensemble_dict['H']['sum']+ref_ensemble_dict['C']['sum'])
# print(slb_ensemble_dict['rutile_O_br_vacant']['sum'])
# print(ads-ref-slb)
def ref_get_formation_energies(ref_dict):
    formation_energyies = {} 
    for key in ref_dict:
        if 'slab' in key:
            continue
        E0_mean = ref_dict[key]['mean']
        E0_std = ref_dict[key]['std']
        composition = string2symbols(key)
        for atom in composition:
            E0_mean -= ref_dict[atom]['mean']
            E0_std -= ref_dict[atom]['std']
        # E0 = round(E0,3)
        formation_energyies[key] = dict()
        formation_energyies[key]['mean'] = E0_mean
        formation_energyies[key]['std'] = E0_std
    return formation_energyies

ref_formation_ensemble = ref_get_formation_energies(ref_ensemble_dict)
# print(ref_formation_ensemble)

def get_potential_energy(reference_dict, ads_slab_dict, slb_dict):
    slb_eng = slb_dict['rutile_O_br_vacant']
    potential_energy_dict = dict()
    for ads in ads_slab_dict.keys():
        E0_mean = ads_slab_dict[ads]['mean']
        # print(E0_mean)
        E0_mean -= slb_eng['mean']

        E0_std = ads_slab_dict[ads]['std']
        E0_std -= slb_eng['std']
        
        composition = string2symbols(ads)
        for atom in composition:
            E0_mean -= reference_dict[atom]['mean']
            E0_std -= reference_dict[atom]['std']
        # print(E0_mean,E0_std)
        # E0 = round(E0,3)
        potential_energy_dict[ads]=dict() 
        potential_energy_dict[ads]['mean'] = E0_mean
        potential_energy_dict[ads]['std'] = E0_std
    return potential_energy_dict

CH_ensemble = get_potential_energy(ref_ensemble_dict, ads_ensemble_dict, slb_ensemble_dict)
# print(CH_ensemble)
# print(ref_ensemble_dict['H'])
# for key in CH_ensemble.keys():
#     print(CH_ensemble[key]['mean'])

# for key in ref_ensemble_dict.keys():
#     print(ref_ensemble_dict[key]['mean'])

# for key in ads_ensemble_dict.keys():
#     print(ads_ensemble_dict[key]['mean'])

# CH2_ensemble = get_potential_energy(ref_dict, CH2_dict, slab_dict)
# CH3_ensemble  = get_potential_energy(ref_dict, CH3_dict, slab_dict)
# CH3_ensemble['H'] = np.array([0])
# ensemble_dict = dict()
# for en_dict in [CH_ensemble, CH2_ensemble, CH3_ensemble]:
#     for k in en_dict.keys():
#         ensemble_dict[k+'_s']=dict()#=en_dict[k]
#         ensemble_dict[k+'_s']['mean'] = en_dict[k].mean()
#         ensemble_dict[k+'_s']['std'] = en_dict[k].std()
# for en_dict in [ref_formation_ensemble]:
# # for en_dict in [ref_dict]:
#     for k in en_dict.keys():
#         ensemble_dict[k+'_g']=dict()#=en_dict[k]
#         ensemble_dict[k+'_g']['mean'] = en_dict[k].mean()
#         ensemble_dict[k+'_g']['std'] = en_dict[k].std()

# cur_dir = os.getcwd()
# file_name =  'direct_ensemble.pkl'
# with open(file_name, 'wb') as handle:
#     pickle.dump(ensemble_dict, handle)
# handle.close()

# with open(file_name, 'rb') as handle:
#     b = pickle.load(handle)
#     print(b['CH3OH_g'])


