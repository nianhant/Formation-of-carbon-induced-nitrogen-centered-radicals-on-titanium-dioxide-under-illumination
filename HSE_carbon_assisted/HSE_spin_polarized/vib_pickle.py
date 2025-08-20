import os
import pickle
import matplotlib.pyplot as plt

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
    return b
    # print(b)
# pickle_load_vib()

spin_polarized_path = '../HSE_ads/HSE_ads.pkl'
with open(spin_polarized_path, 'rb') as handle:
        spin_polarized_eng = pickle.load(handle)
# print(b['ads_slab'])
diff = {}
diff_list = []

cur_eng = pickle_load_vib()
for ads in cur_eng['ads_slab']:
    if ads in spin_polarized_eng['ads_slab']:
        diff[ads] = cur_eng['ads_slab'][ads]-spin_polarized_eng['ads_slab'][ads]
        diff_list.append(diff[ads])
# although total energies are higher after correcting the ex-correlation
print(diff)
plt.plot(diff_list,'.--')
plt.xlabel('adsorbate')
plt.ylabel('difference in total energy (eV)')
plt.savefig('spin_pol_diff.png')

# print(cur_eng)



