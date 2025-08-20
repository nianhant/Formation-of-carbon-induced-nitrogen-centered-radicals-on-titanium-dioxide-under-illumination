import os
import pickle

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def ref_parse_vib_eng(root):
    try:
        f = open(root + '/HSE_energy.txt')
        # f = open(root + '/energy.txt')
        raw = f.read().splitlines()
        f.close()
        eng= float(raw[0])
        return  eng #vib_eng  
    except:
        return 0
# print(ref_parse_vib_eng('ads_slab/CH3_a'))

def vib_eng_to_dict(dir):
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
    # file_name = 'BEEF_spin_paired.pkl'
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
    print(b)
pickle_load_vib()

with open('../HSE_spin_polarized/HSE_spin_polarized.pkl', 'rb') as handle:
    HSE_spin_paired_dict = pickle.load(handle)
# print(HSE_spin_paired_dict)
cur_dict = vib_eng_to_dict('ads_slab')
for key in HSE_spin_paired_dict['ads_slab']:
    cur_dict[key] = HSE_spin_paired_dict['ads_slab'][key]
# print(cur_dict)
family_vib_eng_dict={}
family_vib_eng_dict['ads_slab'] = cur_dict
cur_dir = os.getcwd()
file_name = str(cur_dir).split('/')[-1] + '.pkl'

with open(file_name, 'wb') as handle:
    pickle.dump(family_vib_eng_dict, handle)
    handle.close()

with open(file_name, 'rb') as handle:
    b = pickle.load(handle)
    print(b)




