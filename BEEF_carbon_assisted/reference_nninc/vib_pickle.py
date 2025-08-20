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

def pickle_dump_vib(cur_dir):
    cur_dir = os.getcwd()
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    family_vib_eng_dict = dict()
    for child in os.listdir('reference'):
        path = os.path.join('reference', child)
        if os.path.isdir(path):
            family_vib_eng_dict[child] = ref_parse_vib_eng(path)
            print(ref_parse_vib_eng(path))
    with open(file_name, 'wb') as handle:
        pickle.dump(family_vib_eng_dict, handle)
    handle.close()

pickle_dump_vib('reference')


def pickle_load_vib():
    cur_dir = os.getcwd()
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    # print(file_name)
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    return b
result = pickle_load_vib()
print(result)

# print((result['H2O']-result['H2'])*2)

