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

init_mag = np.zeros(len(image))
image.set_initial_magnetic_moments(magmoms=init_mag)

calc = Espresso(atoms = image, **parameters)

image.set_calculator(calc)



relax = BFGSLineSearch(image,
                       trajectory='opt.traj',
                       logfile='opt.log',
                       restart='opt.pckl')

relax.run(fmax=0.05)

eng = image.get_potential_energy()

t1 = time.time()
print('Time = {} sec'.format(t1-t0))

eng_ensemble = image.get_ensemble_energies()

t2 = time.time()
print('Time = {} sec'.format(time.time()-t2))
run_time = 't1 = {} sec and t2 = {} sec' .format(t1-t0, time.time()-t2)

image.write('converged.traj')

with open('energy.txt', 'w') as f:
    f.write(str(eng))

np.savetxt('ensemble_np.txt',eng_ensemble[0])

with open('contribution.txt', 'w') as f:
    f.write(str(eng_ensemble[1]))

# with open('time.txt', 'w') as f:
#     f.write(str(run_time))

image.calc.close()
