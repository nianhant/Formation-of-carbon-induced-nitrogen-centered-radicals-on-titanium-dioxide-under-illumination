import os
import copy
import pickle
from shutil import copy, move
import numpy as np
from ase.symbols import string2symbols

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def grab_eng(path):
    cur_dir = os.path.realpath(path)
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'energy.txt' in files:
            result = float(readFile(root + '/energy.txt')[0]) 
    return result
            
def ads_slab_eng(path):
    cur_dir = os.path.realpath(path)
    eng_dict={}#dict()
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
            DFT_eng = grab_eng(root)
            # BEEF-ensemble in pw.out is in Ryd
            eng_dict[adsorbate] = np.array(result)*13.605698 + DFT_eng
    return eng_dict

ACS_dict = ads_slab_eng('../ads_slab')
slab_dict = ads_slab_eng('../slab_BEEF')
# print(slab_dict)
ref_dict = ads_slab_eng('../reference_BEEF')
ref_dict['H'] = 0.5*ref_dict['H2']
ref_dict['N'] = 0.5*ref_dict['N2']
ref_dict['O'] = ref_dict['H2O'] - ref_dict['H2']
ref_dict['OH'] = ref_dict['H2O'] - ref_dict['H']
# ref_dict['C'] = ref_dict['CH3OH'] - 4*ref_dict['H'] - ref_dict['O']
ref_dict['NH3'] = ref_dict['N'] + 3*ref_dict['H']
ref_dict.pop('CH3OH')
ref_dict.pop('CH3')
ref_dict.pop('CH4')
ref_dict.pop('CO2')

# print(ref_dict)
def ref_get_formation_energies(reference_dict):
    formation_energyies = {} 
    for key in reference_dict:
        if key == 'slab':
            continue
        E0 = reference_dict[key].copy()
        print(key)
        composition = string2symbols(key)
        for atom in composition:
            E0 -= reference_dict[atom]
        # E0 = round(E0,3)
        formation_energyies[key] = E0
    return formation_energyies

reference_dict={key: value[:] for key, value in ref_dict.items()}
ref_formation_ensemble = ref_get_formation_energies(reference_dict)
# print(ref_formation_ensemble['N2'])

for key in ref_formation_ensemble:
    print(key)
    print('list=',ref_formation_ensemble[key])
    print('*************************************')

def get_potential_energy(reference_dict, ads_slab_dict, slb_dict):
    slb_eng = slb_dict['rutile_O_br_vacant']
    # slb_eng = slb_dict['rutile_C_sub']
    potential_energy_dict = dict()
    for ads in ads_slab_dict.keys():
        # print(ads)
        E0 = ads_slab_dict[ads]
        # print(E0.std())
        E0 -= slb_eng
        # print(E0.std())
        composition = string2symbols(ads)
        for atom in composition:
            # print(atom)
            # print(reference_dict[atom].std())
            E0 -= reference_dict[atom]
        potential_energy_dict[ads] = E0
    return potential_energy_dict

ACS_ensemble = get_potential_energy(ref_dict, ACS_dict, slab_dict)

# print(ACS_ensemble['N2'].mean())
# print(ACS_ensemble['N2'].std())

ACS_ensemble['H'] = np.array([0])

ensemble_dict = dict()
for en_dict in [ACS_ensemble]:
    for k in en_dict.keys():
        ensemble_dict[k+'_s']=dict()
        ensemble_dict[k+'_s']['mean'] = en_dict[k].mean()
        ensemble_dict[k+'_s']['std'] = en_dict[k].std()
for en_dict in [ref_formation_ensemble]:
    for k in en_dict.keys():
        ensemble_dict[k+'_g']=dict()
        ensemble_dict[k+'_g']['mean'] = en_dict[k].mean()
        ensemble_dict[k+'_g']['std'] = en_dict[k].std()



cur_dir = os.getcwd()
file_name = str(cur_dir).split('/')[-2].split('_')[0]+'_'+str(cur_dir).split('/')[-1] + '.pkl'
with open(file_name, 'wb') as handle:
    pickle.dump(ensemble_dict, handle)
handle.close()

# with open(file_name, 'rb') as handle:
#     b = pickle.load(handle)
#     print(b['CH3OH_s'])




 