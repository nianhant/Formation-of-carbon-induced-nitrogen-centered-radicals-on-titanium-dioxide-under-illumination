import os
# import pathlib
from shutil import copy, move

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def generate_parameters(file_name, surface_name, cur_dir, path):
    content = readFile(file_name)
    # cur_dir = cur_dir.split('/')[-1]
    # cur_dir = '''"''' + cur_dir #+ '''"'''
    # new_line = '"outdir": ' + cur_dir + '.log' +'''"''' +',\n'
    print(path)
    with open(path + '/parameters.json', 'w') as modified:
        print(content)
        # content.insert(8,new_line)
        # content = ''.join(content)
        modified.write(content)

def generate_run_sh(file_name, surface_name, path):
    content = readFile(file_name)
    job_name = os.getcwd().split('/')[-1] +'/'+ path.split('/')[-1]
    new_line = '#PBS -N ' + job_name + '\n'
    with open(path + '/run.sh', 'w') as modified:
        content.insert(1,new_line)
        content = ''.join(content)
        modified.write(content)
# sim = read("../systems/N2_rutile_110.traj")
def generate_run_py(file_name, surface_name, path):
    content = readFile(file_name)
    if 'converged.traj' in os.listdir(path):
        new_line = 'sim = read(\'' + 'converged.traj' + '\')\n'
    elif 'opt.traj' in os.listdir(path):
        new_line = 'sim = read(\'' + 'opt.traj' + '\')\n'
    else:
        new_line = 'sim = read(\'' + surface_name + '\')\n'
    print(path, new_line)
    with open(path + '/run.py', 'w') as modified:
        content.insert(16,new_line)
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


copy_script('run.sh', 'reference')
copy_script('run.py', 'reference') 
          
 