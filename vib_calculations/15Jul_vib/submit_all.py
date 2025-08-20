import os
from subprocess import call
import sys
import json

def submit(dir):
    cur_dir=os.path.realpath('.')
    for root, dirs, files in os.walk(dir, topdown=False):
        files = set(files)
        if 'vib.txt' not in files:
            if 'run.sh' in files:
                print('yes')
                os.chdir(os.path.join(root))
                print('run '+root)
                call(["qsub","run.sh"])
                os.chdir(cur_dir)

# submit('slab')
submit('ads_slab')
# submit('reference')
