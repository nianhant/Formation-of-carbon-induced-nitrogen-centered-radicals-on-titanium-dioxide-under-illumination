# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:51:35 2017

@author: benjamin
"""

from ase.build import molecule
from ase.visualize import view
from ase import Atoms

given_molecule = 'N2O'
atoms = molecule(given_molecule)
pos = atoms.get_positions()
L = pos.max() +6
atoms = Atoms(molecule(given_molecule), cell =(L,L,L), positions=pos+L/2)

view(atoms)
atoms.write('POSCAR')
