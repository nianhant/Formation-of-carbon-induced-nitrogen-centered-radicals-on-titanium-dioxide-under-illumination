from ase.build import molecule, bulk
from ase.data.pubchem import pubchem_atoms_search
import numpy as np
from shutil import copy
import os
from ase.build import surface, add_adsorbate, molecule
from ase.spacegroup import crystal
from ase.visualize import view
from ase.io.trajectory import TrajectoryReader
import os
from ase.io import read

atoms = molecule('O2')
max_pos = np.amax(atoms.get_positions(), axis=0)
atoms.set_cell(np.array([10, 10, 10]) + max_pos)
atoms.center()

# atoms.set_initial_magnetic_moments = [0.0, 0.0]
# print(atoms.get_initial_magnetic_moments())
atoms.write(os.path.join('O2.traj'))

def visualize_surf(surf):
    traj = TrajectoryReader(surf)
    surface = traj[0]
    # view(surface)
    traj.close()
    # print(surface)

    return surface

O2 = visualize_surf('O2.traj')
print(O2.get_initial_magnetic_moments())

# visualize_surf('O2.traj')