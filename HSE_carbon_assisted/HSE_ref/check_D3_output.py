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
    for root, dirs, files in os.walk(dir, topdown=False):
        files = set(files)
        if 'sprc-calc.out' in files and 'HSE_energy.txt'  in files:

                check_D3_in_output(root+'/sprc-calc.out')
def check_D3_in_output(file_name):
    f = open(file_name)
    if 'D3' in f.read():
        print(file_name)

# submit('slab')
# submit('ads_slab')
submit('reference')
