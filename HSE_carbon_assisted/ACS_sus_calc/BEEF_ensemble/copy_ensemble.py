import os
from shutil import copy, move

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content


def copy_script(start_path, end_path, target_path):
    folder_name = end_path
    # print(folder_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    if 'ads_slab' in os.listdir(start_path):
        tar ='/ads_slab'
        # L = os.listdir(start_path+'/ads_slab')
        # target_L = os.listdir(target_path+'/ads_slab')
    elif 'reference' in os.listdir(start_path):
        tar ='/reference'
        # L = os.listdir(start_path+'/reference')
        # target_L = os.listdir(target_path+'/reference')
    if 'slab' in end_path:
        tar ='/slab'
        # L = os.listdir(start_path+'/slab')
        # target_L = os.listdir(target_path+'/slab')

    L = os.listdir(start_path+tar)
    target_L = os.listdir(target_path+tar)


    for site in target_L:
        site_path = os.path.join(target_path+tar, site)
        site_destination = folder_name + '/' + site
        if not os.path.exists(site_destination):
                os.mkdir(site_destination)
        if os.path.isdir(site_path):
            child = site_path.split('/')[-1]
            surface_name = site_path + '/' + str(child) +'.traj'
            converged_name = site_path + '/converged.traj'
            ensemble_path = os.path.join(start_path+tar, site)
            ensemble_name = ensemble_path + '/ensemble_np.txt'
            energy_name = ensemble_path + '/energy.txt'
            ads_destination = site_destination +  '/ensemble_np.txt'
            try:
                copy(energy_name, site_destination+'/energy.txt')
                copy(ensemble_name, ads_destination)
            except:
                print('ensemble does not exists:',ads_destination)

copy_script('../ads_slab','ACS_BEEF','../ads_slab')
# copy_script('../CH2_calc','CH2_BEEF','CH2_dft')
# copy_script('../CH3_end_on','CH3_BEEF','CH3_dft')
# copy_script('../02Aug_vib_paired','CH3_BEEF','CH3_dft')
# copy_script('../reference_dft','reference_BEEF','../reference_dft')
# copy_script('../02Aug_vib_paired','slab_BEEF','../02Aug_vib_paired')
