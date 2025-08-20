import os
from ase.io import read
from ase.optimize import BFGSLineSearch #QuasiNewton #geometry optimization algorithm; QuasiNewton links to BFGS line search, which is the best general-purpose optimizer, but other options are available: https://wiki.fysik.dtu.dk/ase/ase/optimize.html
from espresso import iEspresso as Espresso
from espresso.vibespresso import Vibespresso
from ase.constraints import FixAtoms
from ase.vibrations import Vibrations
import numpy as np
import time
import json


image = read('converged.traj')
# setup calculator 
parameters = json.load(open('parameters.json','r'))

calc = Vibespresso(atoms = image, **parameters)

n = 0
df = os.path.abspath("")
mf = df.split('/')[-1].split('_')[0]
n=0
for i in range(len(mf)): #count the number of atoms in the molecule based on the name of the directory 1 levels up
        try:
            n = n + float(mf[i])-1
        except:
            n = n+1


image.set_calculator(calc)

vib = Vibrations(image,indices=range(int(len(image)-n),int(len(image))) ,name='vib.log',nfree=2)
vib.run()
vib.summary(log='vib.txt')
# vib.write_mode(-1)
# image.calc.close()
