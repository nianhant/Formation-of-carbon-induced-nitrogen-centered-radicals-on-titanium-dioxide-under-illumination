from ase.build import molecule, bulk
from ase.data.pubchem import pubchem_atoms_search
import numpy as np
from shutil import copy
import os

name = 'NH2'
atoms = molecule(name)
max_pos = np.amax(atoms.get_positions(), axis=0)
atoms.set_cell(np.array([10, 10, 10]) + max_pos)
atoms.center()

dir_name = name
if not os.path.exists(dir_name):
        os.makedirs(dir_name)
atoms.write(name+'/' +name + '.traj')

# from ase.build import molecule
# from ase.visualize import view
# from ase import Atoms

# given_molecule = 'CH3'
# atoms = molecule(given_molecule)
# pos = atoms.get_positions()
# L = pos.max() +6
# atoms = Atoms(molecule(given_molecule), cell =(L,L,L), positions=pos+L/2)

