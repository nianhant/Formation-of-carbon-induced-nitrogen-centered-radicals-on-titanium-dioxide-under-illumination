import os
import pickle
from ase.symbols import string2symbols

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def ref_parse_vib_eng(root):
    try:
        f = open(root + '/HSE_energy.txt')
        raw = f.read().splitlines()
        f.close()
        eng= float(raw[0])
        return  eng #vib_eng  
    except:
        return 0
# print(ref_parse_vib_eng('ads_slab/CH3_a'))

def vib_eng_to_dict(dir):
    # returns a dictionary[adsorbate]= vib energies
    vib_data = dict()
    for child in os.listdir(dir):
        path = os.path.join(dir, child)
        if os.path.isdir(path):
            adsorbate = str(child).split('_')[0] 
            vib_data[adsorbate] = ref_parse_vib_eng(dir + '/' + child)
    return vib_data

vib_eng_to_dict('ads_slab')
# vib_eng_to_dict('reference')

def pickle_dump_vib():
    cur_dir = os.getcwd()
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    family_vib_eng_dict = dict()
    for child in os.listdir(cur_dir):
        path = os.path.join(cur_dir, child)
        if os.path.isdir(path):
            family_vib_eng_dict[child] = vib_eng_to_dict(path)
    with open(file_name, 'wb') as handle:
        pickle.dump(family_vib_eng_dict, handle)
    handle.close()

pickle_dump_vib()


def pickle_load_vib():
    cur_dir = os.getcwd()
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    # print(b)
    return b
down_sampling_dict = pickle_load_vib()
print(down_sampling_dict['ads_slab']['CH3N'] -down_sampling_dict['slab']['rutile'] )
# with open('../../HSE_ads/HSE_ads.pkl', 'rb') as handle:
#     HSE_ads_dict = pickle.load(handle)
# # print(HSE_ads_dict)

# with open('../../HSE_slab/HSE_slab.pkl', 'rb') as handle:
#     HSE_slab_dict = pickle.load(handle)
# # print(HSE_slab_dict)

# with open('../../HSE_ref/HSE_ref.pkl', 'rb') as handle:
#     ref_eng = pickle.load(handle)['reference']
# kpt_dict = {}
# kpt_dict['ads_slab'] = {}
# kpt_dict['ads_slab']['CH3N'] = HSE_ads_dict['ads_slab']['CH3N']

# kpt_dict['slab'] = {}
# kpt_dict['slab']['rutile'] = HSE_slab_dict['slab']['rutile']
# # print(kpt_dict)
# ################# calculate binding energy
# print(ref_eng)
# # ref_eng = pickle_load_vib('../../../HSE_ref/HSE_ref.pkl')
# ref_eng['O'] =ref_eng['H2O'] - ref_eng['H2']
# ref_eng['H'] = 0.5*ref_eng['H2']
# ref_eng['N'] = 0.5*ref_eng['N2']
# ref_eng['C'] = ref_eng['CH3OH'] - 4*ref_eng['H']-ref_eng['O']
# # print(ref_eng)
# def binding_eng(ads_slab_eng, ref_eng):
#     binding_eng = {}
#     # ref_eng={}
#     for key in ads_slab_eng['ads_slab']:
#         ref_key = key.split('_')[0]
#         if ref_key not in ref_eng:
#             ref_eng[ref_key]=0
#             chem_list = string2symbols(ref_key)
#             for c in chem_list:
#                 ref_eng[ref_key]+=ref_eng[c]
#         try:
#             binding_eng[key] = ads_slab_eng['ads_slab'][key] - ads_slab_eng['slab']['rutile'] - ref_eng[ref_key]
#         except:
#             continue
#     # print(ads_slab_eng)
#     # print(ref_eng)
#     return binding_eng
# print('down sampling (441-> 221):', binding_eng(down_sampling_dict, ref_eng)) 
# print('No down sampling (441)',binding_eng(kpt_dict, ref_eng)) 

# # print('down sampling (441-> 221):', binding_eng(down_sampling_dict, ref_eng)) 
# # print('No down sampling (441)',binding_eng(kpt_dict, ref_eng)) 


