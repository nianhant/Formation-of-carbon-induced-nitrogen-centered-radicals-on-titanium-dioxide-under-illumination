from ase.build import surface, add_adsorbate, molecule
from ase.spacegroup import crystal
from ase.visualize import view
from ase.io.trajectory import TrajectoryReader
from ase.io import read, write
import os
from ase.io import read
import matplotlib.pyplot as plt
# %matplotlib inline

def visualize_surf(surf):
    traj = TrajectoryReader(surf)
    surface = traj[0]
    # print(surface)
#     surface = surface.repeat((3,3,1))
    # view(surface)
    print('image/'+ surf.split('/')[-3]+ '.png')
    file_name = 'image/'+ surf.split('/')[-3]+ '.png'
    write(file_name, surface,rotation='10z,-80x')
    traj.close()

if not os.path.exists('image'):
        os.makedirs('image')
for o in os.listdir('.'):
    if os.path.isdir(o):
        try:
            file =  o + '/test/converged_slab.traj'
            visualize_surf(file)
        except:
            continue
