import os
import pickle

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def ref_parse_vib_eng(root):
    try:
        f = open(root + '/vib.txt')
        raw = f.read().splitlines()
        f.close()
        vib_eng = [] #meV out of the file, converted to eV below
        vib_freq = [] #cm^-1
        for line in raw:
            if '-' not in line and 'eV' not in line:
                d = line.strip()
                d,freq = d.rsplit(' ',1)
                try:
                    vib_freq.append(float(freq))
                    d = d.strip()
                    d,eng = d.rsplit(' ',1)
                    vib_eng.append(float(eng)/10**3) #converting to eV
                except:
                    continue
        return vib_freq#vib_eng#, vib_freq
    except:
        print('No vib.txt available yet')  
# print(ref_parse_vib_eng('ads_slab/CH3_a'))

def vib_eng_to_dict(dir):
    # returns a dictionary[adsorbate]= vib energies
    vib_data = dict()
    for child in os.listdir(dir):
        path = os.path.join(dir, child)
        if os.path.isdir(path):
            adsorbate = str(child).split('_')[0] 
            vib_data[adsorbate] = ref_parse_vib_eng(dir + '/' + child)
    print(vib_data)
    return vib_data

# vib_eng_to_dict( 'ads_slab')
# vib_eng_to_dict('reference')
 
def pickle_dump_vib(path):
    cur_dir = os.getcwd() + '/' + path
    # print(cur_dir)
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    family_vib_eng_dict = dict()
    for child in os.listdir(cur_dir):
        path = os.path.join(cur_dir, child)
        if os.path.isdir(path):
            family_vib_eng_dict[child] = vib_eng_to_dict(path)
    with open(file_name, 'wb') as handle:
        pickle.dump(family_vib_eng_dict, handle)
    handle.close()

pickle_dump_vib('CH3_calc')
pickle_dump_vib('CH2_calc')
pickle_dump_vib('CH_calc')
pickle_dump_vib('H2O_calc')
pickle_dump_vib('pristine')
pickle_dump_vib('Thiel_calc')

def pickle_load_vib(path):
    # cur_dir = os.getcwd()
    cur_dir = os.getcwd() + '/' + path
    file_name = str(cur_dir).split('/')[-1] + '.pkl'
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    print(b['ads_slab']['CH2NHH'])
pickle_load_vib('CH2_calc')

