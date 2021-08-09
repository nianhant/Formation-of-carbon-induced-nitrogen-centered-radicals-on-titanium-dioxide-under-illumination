from ase.io import read
from ase.optimize import BFGSLineSearch #QuasiNewton #geometry optimization algorithm; QuasiNewton links to BFGS line search, which is the best general-purpose optimizer, but other options are available: https://wiki.fysik.dtu.dk/ase/ase/optimize.html
from espresso import iEspresso as Espresso
import numpy as np
import time
import json
image = read('converged.traj')

t0 = time.time()

# setup calculator 
parameters = json.load(open('parameters.json','r'))
# set initial_magmom to 0.1 in C
for atom in image:
    if atom.symbol == 'C':
        atom.magmom = 0.1
print(image.get_initial_magnetic_moments())