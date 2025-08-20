# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 08:47:43 2017

@author: benjamin
"""

#Import all necessary modules
from ase import io
from ase.parallel import paropen as open #ensures that open works in parallel environment
#from ase.optimize import QuasiNewton #geometry optimization algorithm; QuasiNewton links to BFGS line search, which is the best general-purpose optimizer, but other options are available: https://wiki.fysik.dtu.dk/ase/ase/optimize.html
from espresso.vibespresso import vibespresso
from ase.constraints import FixAtoms
from ase.vibrations import Vibrations
import os
#setup calculator


calcargs = dict(xc='BEEF-vdW',
        kpts=(4, 4, 1), #only need 1 kpt in z-direction
        pw=400.,
        dw=4000.,
        spinpol=True,
        beefensemble=True,
        printensemble=True,
        convergence={'energy':1e-6,
                    'mixing':0.05,
                    'maxsteps':100,
                    'diag':'david'},
        startingwfc='atomic',
        smearing='fd', #fermi-dirac electron smearing
        sigma=0.1, #smearing width
        dipole={'status':True}, #dipole corrections True turns them on
        #parflags='-nk 2',
        outdir ='esp.log')

calc = vibespresso(**calcargs)

atoms = io.read('converged_slab.traj') #Read in the structure built by the other script
atoms = io.read('converged_slab.traj') #Read in the structure built by the other script

f = open('../build.py')
txt = f.read()
f.close()
layers,_ = txt.split('\nvacuum =',1)
_,layers = layers.split('layers = ',1)
layers = float(layers.strip())
vacuum,_ = txt.split('\nunfrozen =',1)
_,vacuum = vacuum.rsplit('vacuum = ',1)
vacuum = float(vacuum.strip())
df = os.path.abspath("")
mf = df.split('/')[-3]
n=0
for i in range(len(mf)): #count the number of atoms in the molecule based on the name of the directory 3 levels up
        try:
                n = n + float(mf[i])-1
        except:
                n = n+1

z_cutoff = 3.288*(layers)+vacuum
#d = FixAtoms(mask=[a.z < z_cutoff for a in atoms])
#d = FixAtoms(indices=range[:-n])
#atoms.set_constraint(FixAtoms(indices=range(0,len(atoms)-n)))

atoms.set_calculator(calc)


vib = Vibrations(atoms,indices=range(int(len(atoms)-n),int(len(atoms))) ,name='vib.log',nfree=2)
vib.run()
vib.summary(log='vib.txt')
