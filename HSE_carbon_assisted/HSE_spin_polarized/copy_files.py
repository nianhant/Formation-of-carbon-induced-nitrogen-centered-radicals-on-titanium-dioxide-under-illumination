import os
from shutil import copy, move

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def copy_script():
    cur_dir = os.getcwd()
    folder_name = cur_dir.split('/')[-1]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    L = os.listdir(cur_dir)
    L.remove(folder_name) 
    for site in L: # ads_slab, slab, reference
        site_path = os.path.join(cur_dir, site)
        if os.path.isdir(site_path):
            site_destination = folder_name + '/' + site
            if not os.path.exists(site_destination):
                os.mkdir(site_destination)
            for child in os.listdir(site_path):
                child_path = os.path.join(site_path, child)
                if os.path.isdir(child_path):
                    # surface_name = child_path + '/' + str(child) +'.traj'
                    converged_name = child_path + '/converged.traj'
                    eng_name = child_path + '/HSE_energy.txt'
                    if 'converged.traj' in os.listdir(child_path):
                        ads_destination = site_destination + '/' + child
                        if not os.path.exists(ads_destination):
                            os.mkdir(ads_destination)

                        copy(converged_name, ads_destination)
                        # copy(surface_name, ads_destination)
                        copy(eng_name, ads_destination)

copy_script()