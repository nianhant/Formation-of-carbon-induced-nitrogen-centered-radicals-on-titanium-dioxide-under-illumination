import os
from copy import deepcopy as dc
from sparc.sparc_core import SPARC
from ase.calculators.calculator import CalculatorSetupError
from sparc.ion import write_ion, read_ion
from ase.build import bulk, molecule
from ase.calculators.calculator import compare_atoms
from ase.visualize import view
from ase.constraints import FixAtoms, FixedLine, FixedPlane
import numpy as np
from getpseudo import getpseudo
from ase.io import read, write
import json

#setting the path for Atoms object

sim = read('converged.traj')

# parameters = json.load(open('parameters.json','r'))
# calc = SPARC(**parameters)
calc = SPARC(KPOINT_GRID=[1,1,1], 
             EXCHANGE_CORRELATION="HSE", 
             TOL_FOCK=5e-05, h = 0.05, 
             PRINT_FORCES=1, PRINT_ATOMS=1, PRINT_EIGEN=1, 
             MAXIT_FOCK=1000,  ACE_FLAG=1, TOL_SCF=1E-6,
             EXX_ACE_MEM=1, EXX_DIVERGENCE="AUXILIARY", 
             EXX_RANGE_FOCK=0.106, EXX_RANGE_PBE=0.106, 
             BOUNDARY_CONDITION=[True,True,False],
             EXX_ACE_VALENCE_STATES= 10000,
             pseudo_dir=getpseudo("espresso_jagriti#psps_mostafa#21#10#06_PSP8"))
sim.set_calculator(calc)
energy = sim.get_potential_energy()
print(energy)
with open('HSE_energy.txt', 'w') as f:
    f.write(str(energy))