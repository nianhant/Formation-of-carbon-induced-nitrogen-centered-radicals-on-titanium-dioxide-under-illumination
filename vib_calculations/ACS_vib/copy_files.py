import os
from shutil import copy, move

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def copy_script(path):
    cur_dir = os.getcwd() + '/' + path
    folder_name = cur_dir.split('/')[-1].split('_')[0] + '_updated_dft'
    # print(folder_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    L = os.listdir(cur_dir)
    # print(L)
    # print(folder_name)
    if folder_name in L:
        L.remove(folder_name)
    # print(L) 
    for site in L: # ads_slab, slab, reference
        site_path = os.path.join(cur_dir, site)
        if os.path.isdir(site_path):
            site_destination = folder_name + '/' + site
            if not os.path.exists(site_destination):
                # print(site_destination)
                os.mkdir(site_destination)
            for child in os.listdir(site_path):
                # print(site_path)
                child_path = os.path.join(site_path, child)
                if os.path.isdir(child_path):
                    if path == 'H2O_calc' and child.split('_')[0][-2:] == 'HO':
                        surface_name = child_path + '/' + (child.split('_')[0][:-2] + 'OH_'+child.split('_')[1]) +'.traj'
                        # print(surface_name)
                    else:
                        surface_name = child_path + '/' + str(child) +'.traj'
                    converged_name = child_path + '/converged.traj'
                    eng_name = child_path + '/energy.txt'
                    if 'converged.traj' in os.listdir(child_path):
                        ads_destination = site_destination + '/' + child
                        # print(ads_destination)
                        if not os.path.exists(ads_destination):
                            os.mkdir(ads_destination)
                        copy(converged_name, ads_destination)
                        copy(surface_name, ads_destination)
                        copy(eng_name, ads_destination)
copy_script('ads_slab')
