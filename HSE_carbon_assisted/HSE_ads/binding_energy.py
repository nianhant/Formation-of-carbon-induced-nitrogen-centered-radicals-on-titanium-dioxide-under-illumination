import os
import pickle
from ase.symbols import string2symbols

def pickle_load_vib(file_name):
    # cur_dir = path
    # # cur_dir = os.getcwd()
    # file_name = str(cur_dir).split('/')[-1] #+ '.pkl'
    # print(file_name)
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    return b

ads_pkl_file = os.getcwd().split('/')[-1]+'.pkl'
ads_slab_eng = pickle_load_vib(ads_pkl_file)
print(ads_slab_eng)

slab_eng = pickle_load_vib('../HSE_slab/HSE_slab.pkl')
ref_eng = pickle_load_vib('../HSE_ref/HSE_ref.pkl')
ref_eng =ref_eng['reference']
# print(slab_eng)
ref_eng['O'] =ref_eng['H2O'] - ref_eng['H2']
# ref_eng['O'] = 0.5*ref_eng['O2']
ref_eng['H'] = 0.5*ref_eng['H2']
ref_eng['N'] = 0.5*ref_eng['N2']
ref_eng['C'] =ref_eng['CH3OH'] - 2*ref_eng['H2'] - ref_eng['O']

binding_eng = {}
# for kpt  in kpt_ads_slab_eng.keys():
#     ads_slab_eng = kpt_ads_slab_eng[kpt]
# binding_eng[kpt] ={}
for key in ads_slab_eng['ads_slab']:
    print(key)
    ref_key = key.split('_')[0]
    if ref_key not in ref_eng:
        ref_eng[ref_key]=0
        chem_list = string2symbols(ref_key)
        for c in chem_list:
            ref_eng[ref_key]+=ref_eng[c]
    try:
        binding_eng[key] = ads_slab_eng['ads_slab'][key] - slab_eng['slab']['rutile'] - ref_eng[ref_key]
    except:
        continue
# print((binding_eng) )
binding_eng_file_name = 'HSE_'+os.getcwd().split('/')[-1]+'_binding'+'.pkl'
with open(binding_eng_file_name, 'wb') as handle:
    pickle.dump(binding_eng, handle)
handle.close()
for key in binding_eng:
    ads_eng = binding_eng[key]
    # print(key)
    # for ads in ads_eng:
    #     if 'O2' in ads and ads_eng[ads] >= -1 and ads_eng[ads] <= 2:
    #         print(ads, ads_eng[ads], '\n')
    #     elif 'N2'in ads and ads_eng[ads] <= 0:
    #         # print(key)
    #         print(ads, ads_eng[ads], '\n')
            

    # print(key, binding_eng[key])
    # print('\n')
print(binding_eng)