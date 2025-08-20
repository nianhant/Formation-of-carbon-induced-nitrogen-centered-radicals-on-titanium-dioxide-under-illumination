import os
from ase import io
from ase.visualize import view
from ase.constraints import FixAtoms, FixedLine, FixBondLengths
from ase import Atoms
import numpy as np
from ase.build import surface, add_adsorbate, molecule
from ase import io
from ase.visualize import view
from ase.constraints import FixAtoms
import os
from ase import io
from ase.visualize import view
from ase.constraints import FixAtoms, FixedLine, FixBondLengths
from ase import Atoms
import numpy as np

from ase import *
from ase.build import surface, add_adsorbate, molecule
from ase.spacegroup import crystal
from ase.visualize import view
from ase.io.trajectory import TrajectoryReader
from ase.build.tools import sort
from ase.constraints import FixAtoms
import numpy as np

#### perslab
y_num = 3
layers = 4
vacuum = 6
unfrozen = 3
rutile = io.read('Bulk_Rutile.json')
slb = surface(rutile,indices=(1,1,0),layers=layers,vacuum=vacuum)


#move around some unruly atoms
pos = slb[len(slb)-1].get('position') +[0,0,-3.288*layers]
slb[len(slb)-1].set('position',pos)
pos = slb[len(slb)-2].get('position') +[0,0,-3.288*layers]
slb[len(slb)-2].set('position',pos)
pos = slb[len(slb)-4].get('position') +[0,0,-3.288*layers]
slb[len(slb)-4].set('position',pos)

slb = slb*(1,y_num,1)
slb = sort(slb,tags = slb.positions[:,1])

del_list = []
for i in range(len(slb)):
    if slb[i].position[2] <= 7.304:
        print(i)
        del_list.append(i)
del_list.reverse()
for i in (del_list):
    del slb[i]
    
ov_pos = slb.positions[20]
del slb[20]
z_cutoff = 10.6#3.288*(layers-unfrozen)+vacuum
d = FixAtoms(mask=[a.z < z_cutoff for a in slb])
slb.set_constraint(d)
perslab = slb
# perslab = perslab.repeat((2,2,1))
# view(perslab)

dir_name = 'slab/perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/perslab.traj'
# perslab.write(file_name)
# print(file_name, '\ngeneration done')

### H2O
H2O_perslab = perslab.copy()
H2O = molecule('H2O')
H2O.positions*=-1

diff = ov_pos - H2O.positions[0]
H2O.positions += diff
H2O_perslab += H2O

dir_name = 'ads_slab/H2O_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/H2O_perslab.traj'
H2O_perslab.write(file_name)
print(file_name, '\ngeneration done')

## HH
HH_perslab = perslab.copy()
H = molecule('H')

H.positions = HH_perslab.positions[37]
H.positions[0][2] += 1
HH_perslab += H
H.positions = HH_perslab.positions[2]
H.positions[0][2] += 1
HH_perslab += H

dir_name = 'ads_slab/HH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/HH_perslab.traj'
HH_perslab.write(file_name)
print(file_name, '\ngeneration done')

# N2 on Hyd_perslab
N2HH_perslab = HH_perslab.copy()
N2 = molecule('N2')

adsorbate = molecule('N2')
d = 0.5
add_adsorbate(N2HH_perslab,adsorbate, d, position= ov_pos[:2])

dir_name = 'ads_slab/N2HH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/N2HH_perslab.traj'
N2HH_perslab.write(file_name)
print(file_name, '\ngeneration done')

### N-NH
HNNH_perslab = perslab.copy()
H = molecule('H')

H.positions = HNNH_perslab.positions[37]
H.positions[0][2] += 1
HNNH_perslab += H
N2 = molecule('N2')

adsorbate = molecule('N2')
d = 0.5
add_adsorbate(HNNH_perslab,adsorbate, d, position= ov_pos[:2])

adsorbate = molecule('H')
pos = ov_pos[:2]
pos[1] -= 1
add_adsorbate(HNNH_perslab,adsorbate, d, position= pos)

dir_name = 'ads_slab/HNNH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/HNNH_perslab.traj'
HNNH_perslab.write(file_name)
print(file_name, '\ngeneration done')

# N-NH2
NNH2_perslab = HNNH_perslab.copy()
NNH2_perslab.positions[53] = NNH2_perslab.positions[54]
NNH2_perslab.positions[53][1] += 1
NNH2_perslab.positions[56][2] += 0.5
NNH2_perslab.positions[53][2] += 0.5

dir_name = 'ads_slab/NNH2_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NNH2_perslab.traj'
NNH2_perslab.write(file_name)
print(file_name, '\ngeneration done')

# NNH2HH
NNH2HH_perslab = HH_perslab.copy()
NNH2HH_perslab+= NNH2_perslab[53:57]

dir_name = 'ads_slab/NNH2HH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NNH2HH_perslab.traj'
NNH2HH_perslab.write(file_name)
print(file_name, '\ngeneration done')

# NH2NHH
NH2NHH_perslab = N2HH_perslab.copy()
del NH2NHH_perslab[55]

NH2 = molecule('NH2')
NH2.positions *=-1
adsorbate = NH2
pos = NH2NHH_perslab.positions[34]
d = 0.
add_adsorbate(NH2NHH_perslab,adsorbate, d, position= pos[:2])

dir_name = 'ads_slab/NH2NHH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH2NHH_perslab.traj'
NH2NHH_perslab.write(file_name)
print(file_name, '\ngeneration done')

#NH2HNH_perslab
NH2HNH_perslab =  NH2NHH_perslab.copy()
NH2HNH_perslab.positions[53] = NH2HNH_perslab.positions[55]
NH2HNH_perslab.positions[53][2]+= 1

dir_name = 'ads_slab/NH2HNH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH2HNH_perslab.traj'
NH2HNH_perslab.write(file_name)
print(file_name, '\ngeneration done')

#NH2NH2
ov_pos = np.array([3.40835491e-04, 2.98130111e+00, 1.71718295e+01])

NH2NH2_perslab = NH2HNH_perslab.copy()
del NH2NH2_perslab[53:56]
NH2 = molecule('NH2')
NH2.positions *=-1
adsorbate = NH2
pos = ov_pos
d = -0.2
add_adsorbate(NH2NH2_perslab,adsorbate, d, position= pos[:2])

dir_name = 'ads_slab/NH2NH2_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH2NH2_perslab.traj'
NH2NH2_perslab.write(file_name)
print(file_name, '\ngeneration done')


#NH2NH2HH
NH2NH2HH_perslab = NH2NH2_perslab.copy()
H = molecule('H')
H.positions = NH2NH2HH_perslab.positions[37]
H.positions[0][2] += 1
NH2NH2HH_perslab += H
H.positions = NH2NH2HH_perslab.positions[2]
H.positions[0][2] += 1
NH2NH2HH_perslab += H

dir_name = 'ads_slab/NH2NH2HH_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH2NH2HH_perslab.traj'
NH2NH2HH_perslab.write(file_name)
print(file_name, '\ngeneration done')

#NH2NH3H
NH2NH3H_perslab = NH2NH2HH_perslab.copy()
del NH2NH3H_perslab[56:60]

ov_pos = np.array([3.40835491e-04, 2.98130111e+00, 1.71718295e+01])
NH3 = molecule('NH3')
NH3.positions *=-1
adsorbate = NH3
pos = ov_pos
d = -0.2
add_adsorbate(NH2NH3H_perslab,adsorbate, d, position= pos[:2])

dir_name = 'ads_slab/NH2NH3H_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH2NH3H_perslab.traj'
NH2NH3H_perslab.write(file_name)
print(file_name, '\ngeneration done')

# NH3NH2H_perslab
NH3NH2H_perslab = NH2NH3H_perslab.copy()
del NH3NH2H_perslab[57:61]
ov_pos = np.array([3.40835491e-04, 2.98130111e+00, 1.71718295e+01])
NH2 = molecule('NH2')
NH2.positions *=-1
adsorbate = NH2
pos = ov_pos
d = -0.2
# print(pos)
add_adsorbate(NH3NH2H_perslab,adsorbate, d, position= pos[:2])

del NH3NH2H_perslab[53:56]
NH3 = molecule('NH3')
NH3.positions *=-1
adsorbate = NH3
pos = NH3NH2H_perslab.positions[34]
d = 0.
add_adsorbate(NH3NH2H_perslab,adsorbate, d, position= pos[:2])
# view(NH3NH2H_perslab)


dir_name = 'ads_slab/NH3NH2H_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH3NH2H_perslab.traj'
NH3NH2H_perslab.write(file_name)
print(file_name, '\ngeneration done')

#NH3NH3
NH3NH3_perslab = NH3NH2H_perslab.copy()
del NH3NH3_perslab[53:57]

ov_pos = np.array([3.40835491e-04, 2.98130111e+00, 1.71718295e+01])
NH3 = molecule('NH3')
NH3.positions *=-1
adsorbate = NH3

pos = ov_pos
d = -0.2
add_adsorbate(NH3NH3_perslab,adsorbate, d, position= pos[:2])

dir_name = 'ads_slab/NH3NH3_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH3NH3_perslab.traj'
NH3NH3_perslab.write(file_name)
print(file_name, '\ngeneration done')

# NH3
NH3_perslab = NH3NH3_perslab.copy()
del NH3_perslab[57:61]

dir_name = 'ads_slab/NH3_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/NH3_perslab.traj'
NH3_perslab.write(file_name)
print(file_name, '\ngeneration done')


# NH3 at Ov

NH3_perslab = NH3NH3_perslab.copy()
del NH3_perslab[53:57]
dir_name = 'ads_slab/H3N_perslab' 
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_name = dir_name + '/H3N_perslab.traj'
NH3_perslab.write(file_name)
print(file_name, '\ngeneration done')
