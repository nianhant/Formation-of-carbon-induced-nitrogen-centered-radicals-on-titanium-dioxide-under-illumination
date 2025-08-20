import os
from ase.io import read

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def check_vib_text(path):
    cur_dir = os.path.realpath(path)
    dir_set = set(os.listdir(cur_dir))
    # print(dir_set)
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'vib.txt' in files:
            dir_name = root.split('/')[-1]
            dir_set.remove(dir_name)
            # print(dir_name)
    print(dir_set)
    return dir_set
# check_vib_text('ads_slab')
# check_vib_text('slab')
# check_vib_text('reference')


def check_empty(path):
    incomplete_calc_dir = check_vib_text(path)
    for ads in incomplete_calc_dir:
        cur_dir = os.path.realpath(path+'/'+ ads+ '/vib.log')
        for root, dirs, files in os.walk(cur_dir, topdown=True):
            files = set(files)
            for file in files:
                result = readFile(root +'/'+file)
                if len(result) == 0:
                    print(root +'/'+file)
                    os.remove(root +'/'+file)
            

check_empty('ads_slab')
# check_empty('slab')
# check_empty('reference')