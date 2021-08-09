from ase.io import read
from ase.optimize import BFGSLineSearch #QuasiNewton #geometry optimization algorithm; QuasiNewton links to BFGS line search, which is the best general-purpose optimizer, but other options are available: https://wiki.fysik.dtu.dk/ase/ase/optimize.html
from espresso import iEspresso as Espresso
import numpy as np
import time
import json

# setup calculator 
parameters = json.load(open('parameters.json','r'))
# set initial_magmom to 0.1 in C
for atom in image:
    if atom.symbol == 'C':
        atom.magmom = 0.6
    if atom.symbol == 'N':
        atom.magmom = 0.6
# print(image.get_initial_magnetic_moments())

calc = Espresso(atoms = image, **parameters)

image.set_calculator(calc)

relax = BFGSLineSearch(image,
                       trajectory='opt.traj',
                       logfile='opt.log',
                       restart='opt.pckl')

relax.run(fmax=0.05)

eng = image.get_potential_energy()

eng_ensemble = image.get_ensemble_energies()

image.write('converged.traj')

with open('energy.txt', 'w') as f:
    f.write(str(eng))

np.savetxt('ensemble_np.txt',eng_ensemble[0])


image.calc.close()
