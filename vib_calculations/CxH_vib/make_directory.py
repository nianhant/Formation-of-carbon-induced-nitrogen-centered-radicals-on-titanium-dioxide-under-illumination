import os
# import pathlib
from shutil import copy, move

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def generate_parameters(file_name, surface_name, cur_dir, path):
    content = readFile(file_name)
    cur_dir = cur_dir.split('/')[-1]
    cur_dir = '''"''' + cur_dir #+ '''"'''
    new_line = '"outdir": ' + cur_dir + '.log' +'''"''' +',\n'
    print(path)
    with open(path + '/parameters.json', 'w') as modified:
        content.insert(8,new_line)
        content = ''.join(content)
        modified.write(content)

def generate_run_sh(file_name, surface_name, path):
    content = readFile(file_name)
    job_name = os.getcwd().split('/')[-1] +'/'+ path.split('/')[-1]
    print(job_name)
    new_line = '#PBS -N ' + job_name + '\n'
    with open(path + '/run.sh', 'w') as modified:
        content.insert(1,new_line)
        content = ''.join(content)
        modified.write(content)

def generate_run_py(file_name, surface_name, path):
    content = readFile(file_name)
    # if 'converged.traj' in os.listdir(path):
    new_line = 'image = read(\'' + 'converged.traj' + '\')\n'
    print(path, file_name, new_line)
    with open(path + '/run.py', 'w') as modified:
        content.insert(12,new_line)
        content = ''.join(content)
        modified.write(content)
     
def copy_script(file_name, dir):
    cur_dir = os.getcwd()
    for child in os.listdir(dir):
        path = os.path.join(dir, child)
        if os.path.isdir(path):
            surface_name = str(child) +'.traj'
            # if not file_name in os.listdir(path):
            if file_name == 'run.sh':
                generate_run_sh(file_name, surface_name, path)
            elif file_name == 'run.py':
                generate_run_py(file_name, surface_name, path)
            elif file_name == 'parameters.json':
                generate_parameters(file_name, surface_name, cur_dir, path)


    print('File generation completed!')


# copy_script('run.sh', 'C_calc/ads_slab')
# copy_script('run.py', 'C_calc/ads_slab')
# copy_script('parameters.json', 'C_calc/ads_slab')

# copy_script('run.sh', 'CH_calc/ads_slab')
# copy_script('run.py', 'CH_calc/ads_slab')
# copy_script('parameters.json', 'CH_calc/ads_slab')

copy_script('run.sh', 'CH2_calc/ads_slab')
copy_script('run.py', 'CH2_calc/ads_slab')
copy_script('parameters.json', 'CH2_calc/ads_slab')

# copy_script('run.sh', 'CH3_calc/ads_slab')
# copy_script('run.py', 'CH3_calc/ads_slab')
# copy_script('parameters.json', 'CH3_calc/ads_slab')

# copy_script('run.sh', 'H2O_calc/ads_slab')
# copy_script('run.py', 'H2O_calc/ads_slab')
# copy_script('parameters.json', 'H2O_calc/ads_slab')

# copy_script('run.sh', 'pristine/ads_slab')
# copy_script('run.py', 'pristine/ads_slab')
# copy_script('parameters.json', 'pristine/ads_slab')


# copy_script('run.sh', 'Thiel_calc/ads_slab')
# copy_script('run.py', 'Thiel_calc/ads_slab')
# copy_script('parameters.json', 'Thiel_calc/ads_slab')
