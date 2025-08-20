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
    # print(surface.get_positions())
#     surface = surface.repeat((3,3,1))
    # view(surface)
    name = surf.split('/')[1]+ '_'+surf.split('/')[-2]
    print('image/'+name + '.png')
    file_name = 'image/'+ name+ '.png'
    write(file_name, surface,rotation='60z,-80x')
    traj.close()

if not os.path.exists('image'):
        os.makedirs('image')
for o in os.listdir('.'):
    surf_path = os.path.join('.', o)
    if os.path.isdir(surf_path):
        for ads in os.listdir(surf_path):
            ads_path = os.path.join(surf_path, ads)
            try:
                # file =  ads_path + '/'+ads+'.traj'
                file =  ads_path + '/converged.traj'
                print(file)
                visualize_surf(file)
            except:
                continue

# try:
#                 file =  ads_path + '/converged.traj'
#                 visualize_surf(file)
#             except:
#                 continue