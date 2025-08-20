import os
from subprocess import call
import sys
import json
from shutil import copy, move
import re
import pickle


def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def submit(dir):
    cur_dir=os.path.realpath('.')
    mag_dict = {}
    for root, dirs, files in os.walk(dir, topdown=False):
        files = set(files)
        file_name = 'pw.out'
        if file_name in files and '.log' in root:
            # print(root)
            if check_magnetization_in_output(root+'/'+ file_name) != None:
                ads = root.split('/')[-2]
                mag_dict[ads] = check_magnetization_in_output(root+'/'+ file_name)
    print(mag_dict)
    with open('BEEF_carbon_mag.pkl', 'wb') as handle:
        pickle.dump(mag_dict, handle)
    handle.close()

                # check_D3_in_output(root+'/sprc-calc.out')
def check_magnetization_in_output(file_name):
    f = open(file_name)
    # print( f.readlines())
    f_reversed = f.readlines()[::-1]
    for i in range(len(f_reversed)):
        if 'total magnetization' in f_reversed[i]:
            last_line = f_reversed[i]
            # info = last_line.strip()
            info = last_line.split(' ')
            info = [x for x in info if x != '']
            # print(file_name, info[3])
            return float(info[3])
            # else:
            #     return None


# submit('slab')
submit('ads_slab')
# submit('reference')
