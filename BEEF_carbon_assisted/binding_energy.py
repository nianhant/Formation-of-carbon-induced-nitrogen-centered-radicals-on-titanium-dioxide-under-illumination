import os
import pickle
from ase.symbols import string2symbols


def pickle_load_vib(file_name):
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    return b
 
ads_pkl_file = os.getcwd().split('/')[-1]+'.pkl'
ads_slab_eng = pickle_load_vib(ads_pkl_file)

 
ref_eng = pickle_load_vib('reference_nninc/reference_nninc.pkl')
ref_eng['H'] = 0.5*ref_eng['H2']
ref_eng['N'] = 0.5*ref_eng['N2']
ref_eng['O'] = ref_eng['H2O'] - ref_eng['H2']
ref_eng['C'] = ref_eng['CH3OH'] - 4*ref_eng['H'] - ref_eng['O']
binding_eng = {}
for key in ads_slab_eng['ads_slab']:
    ref_key = key.split('_')[0]
    if ref_key not in ref_eng:
        ref_eng[ref_key]=0
        chem_list = string2symbols(ref_key)
        for c in chem_list:
            ref_eng[ref_key]+=ref_eng[c]
    binding_eng[key] = ads_slab_eng['ads_slab'][key] - ads_slab_eng['slab']['slab'] - ref_eng[ref_key]
binding_eng_file_name = os.getcwd().split('/')[-1]+'_binding'+'.pkl'
with open(binding_eng_file_name, 'wb') as handle:
    pickle.dump(binding_eng, handle)
handle.close()
for key in binding_eng:
    ads_eng = binding_eng[key]

# print(binding_eng)
######################################################
spin_paired_file = 'BEEF_spin_paired.pkl'

ads_slab_eng_spin_paired = pickle_load_vib(spin_paired_file)
ads_slab_eng_spin_paired['ads_slab']['CH3N2'] = -39989.238027848674
# print(ads_slab_eng_spin_paired)

spin_paired_binding_eng = {}
for key in ads_slab_eng_spin_paired['ads_slab']:
    ref_key = key.split('_')[0]
    if ref_key not in ref_eng:
        ref_eng[ref_key]=0
        chem_list = string2symbols(ref_key)
        for c in chem_list:
            ref_eng[ref_key]+=ref_eng[c]
    spin_paired_binding_eng[key] = ads_slab_eng_spin_paired['ads_slab'][key] - ads_slab_eng['slab']['slab'] - ref_eng[ref_key]
binding_eng_file_name = 'BEEF_spin_paired_binding'+'.pkl'
with open(binding_eng_file_name, 'wb') as handle:
    pickle.dump(spin_paired_binding_eng, handle)
handle.close()
for key in spin_paired_binding_eng:
    ads_eng = spin_paired_binding_eng[key]

# print(spin_paired_binding_eng)

diff_dict ={}
for key in binding_eng:
    ads = key.split('_')[0]
    if ads in spin_paired_binding_eng:
        diff_dict[key] = spin_paired_binding_eng[ads] - binding_eng[key]
print(diff_dict)