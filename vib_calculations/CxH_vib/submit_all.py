import os
from subprocess import call
import sys
import json

def submit(dir):
    cur_dir=os.path.realpath('.')
    for root, dirs, files in os.walk(dir, topdown=False):
        files = set(files)
        if 'vib.txt' not in files and 'out_equi.tgz' not in files:
            if 'run.sh' and 'converged.traj' in files:
                print('yes')
                os.chdir(os.path.join(root))
                print('run '+root)
                call(["qsub","run.sh"])
                os.chdir(cur_dir)

# submit('C_calc/ads_slab')

# submit('CH_calc/ads_slab')
submit('CH2_calc/ads_slab')
# submit('CH3_calc/ads_slab')

# submit('H2O_calc/ads_slab')
# submit('pristine/ads_slab')

# submit('Thiel_calc/ads_slab')

 