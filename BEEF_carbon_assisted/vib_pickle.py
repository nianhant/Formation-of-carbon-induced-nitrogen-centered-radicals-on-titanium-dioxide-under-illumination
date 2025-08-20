import os
import pickle

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def ref_parse_vib_eng(root):
    try:
        f = open(root + '/energy.txt')
        raw = f.read().splitlines()
        f.close()
        eng= float(raw[0])
        return  eng #vib_eng  
    except:
        return 0

def pickle_dump_vib(path):
    cur_dir = path
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    family_vib_eng_dict = dict()
    family_vib_eng_dict['ads_slab'] = {}
    family_vib_eng_dict['slab'] = {}

    for ads_folder in os.listdir(path+'/ads_slab'):
        family_vib_eng_dict['ads_slab'][ads_folder] = ref_parse_vib_eng(path+'/ads_slab/'+ads_folder)
        # print(path+'/ads_slab/'+ads_folder)
        # print(ref_parse_vib_eng(path+'/ads_slab/'+ads_folder))
    for slab_folder in os.listdir(path+'/slab'):
        family_vib_eng_dict['slab'][slab_folder] = ref_parse_vib_eng(path+'/slab/'+slab_folder)
        # print(path+'/slab/'+slab_folder)
        # print(ref_parse_vib_eng(path+'/slab/'+slab_folder))
    with open(file_name, 'wb') as handle:
        pickle.dump(family_vib_eng_dict, handle)
    handle.close()
# path = 'slab'
cur_dir = os.getcwd()
pickle_dump_vib(cur_dir)


def pickle_load_vib():
    cur_dir = os.getcwd()
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    print(b)
pickle_load_vib()

