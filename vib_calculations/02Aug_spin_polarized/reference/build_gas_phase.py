from ase.build import molecule, bulk
from ase.data.pubchem import pubchem_atoms_search
import numpy as np
from shutil import copy
import os

atoms = molecule('CH4')
max_pos = np.amax(atoms.get_positions(), axis=0)
atoms.set_cell(np.array([10, 10, 10]) + max_pos)
atoms.center()

dir_name = 'CH4'
if not os.path.exists(dir_name):
        os.makedirs(dir_name)
atoms.write('CH4/CH4.traj')
