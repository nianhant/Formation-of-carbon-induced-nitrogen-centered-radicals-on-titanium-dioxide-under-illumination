import os
from subprocess import call
import sys
import json
from shutil import copy, move
import re


def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def submit(dir):
    cur_dir=os.path.realpath('.')
    mag_dict = {}
    for root, dirs, files in os.walk(dir, topdown=False):
        files = set(files)
        file_name = 'sprc-calc.out'
        if file_name in files:
                if check_magnetization_in_output(root+'/'+ file_name):
                    ads = root.split('/')[-1]
                    mag = check_magnetization_in_output(root+'/'+ file_name)
                    if abs(mag) >= 0.01:
                        mag_dict[ads] = mag
    print(mag_dict)

                # check_D3_in_output(root+'/sprc-calc.out')
def check_magnetization_in_output(file_name):
    f = open(file_name)
    # print( f.readlines())
    f_reversed = f.readlines()[::-1]
    for i in range(len(f_reversed)):
        if 'Total number of SCF:' in f_reversed[i]:
            last_line = f_reversed[i+1]
            info = last_line.split(' ')
            info = [x for x in info if x != '']
            if len(info) == 5:
                return float(info[2])
            else:
                return None


# submit('slab')
submit('ads_slab')
# submit('reference')
