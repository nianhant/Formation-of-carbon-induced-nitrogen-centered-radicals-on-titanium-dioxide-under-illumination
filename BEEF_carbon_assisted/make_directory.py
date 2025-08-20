import os
import json
from shutil import copy, move

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

def generate_parameters(file_name, surface_name, cur_dir, path):
    f = open(file_name, 'r')
    content = json.load(f)
    cur_dir = cur_dir.split('/')[-1]
    content['outdir'] = cur_dir + '.log' 
    if 'O2' in surface_name:
        content['spinpol']='True'
    # print(content['spinpol'])
    with open(path + '/parameters.json', 'w') as outfile:
        # print(content['spinpol'])
        json.dump(content, outfile)

def generate_run_sh(file_name, surface_name, path):
    content = readFile(file_name)
    job_name = os.getcwd().split('/')[-1] +'/'+ path.split('/')[-1]
    new_line = '#PBS -N ' + job_name + '\n'
    with open(path + '/run.sh', 'w') as modified:
        content.insert(1,new_line)
        content = ''.join(content)
        modified.write(content)

def new_trajectory_name(path):
    max_traj = 0
    for file in os.listdir(path):
        if file.startswith('opt') and file.endswith('traj'):
            # opt_traj_list.append(file)
            if file[3] != '.':
                curr_traj = int(file[3])
                if curr_traj >= max_traj:
                    max_traj = curr_traj
    new_traj = ' \'opt'+str(max_traj+1)+'.traj\''
    new_traj_line = 'traj_file = '+ new_traj
    return max_traj
    # return new_traj_line

def generate_run_py(file_name, surface_name, path):
    content = readFile(file_name)
    if 'O2' in surface_name:
        content[11] = '#'+content[11]
        content[10] = '#'+content[10]
    new_line = 'image = read(\'' + surface_name + '\')\n'
    max_traj = new_trajectory_name(path)
    if 'converged.traj' in os.listdir(path):
        new_line = 'image = read(\'' + 'converged.traj' + '\')\n'
    # else:
    # for file in os.listdir(path):
    #     if file.startswith('opt') and file.endswith('traj'):
    #         new_line = 'image = read(\'opt' + str(max_traj) + '.traj\')\n' 
    #         break
    # new_line = 'image = read(\'' + 'opt'+str(max_traj)+'.traj\'' + ')\n'
    
    new_traj_line = 'traj_file = '+ ' \'opt'+str(max_traj+1)+'.traj\''
    
    print(path, new_line)
    # print(path, new_traj_line)
    with open(path + '/run.py', 'w') as modified:
        content.insert(6,new_line)
        content.insert(18,new_traj_line)
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


# copy_script('run.sh', 'ads_slab')
# copy_script('run.py', 'ads_slab')
# copy_script('parameters.json', 'ads_slab')

# copy_script('run.sh', 'slab')
# copy_script('run.py', 'slab')
# copy_script('parameters.json', 'slab')

copy_script('run.sh', 'ACS_sus_calc/ads_slab')
copy_script('run.py', 'ACS_sus_calc/ads_slab')
copy_script('parameters.json', 'ACS_sus_calc/ads_slab')
           
 # import os
# import json
# from shutil import copy, move

# def readFile(path):
#     f = open(path, 'r')
#     content = f.readlines()
#     return content

# def generate_parameters(file_name, surface_name, cur_dir, path):
#     f = open(file_name, 'r')
#     content = json.load(f)
#     cur_dir = cur_dir.split('/')[-1]
#     content['outdir'] = cur_dir + '.log' 
#     if 'O2' in surface_name:
#         content['spinpol']='True'
#     # print(content['spinpol'])
#     with open(path + '/parameters.json', 'w') as outfile:
#         # print(content['spinpol'])
#         json.dump(content, outfile)

# def generate_run_sh(file_name, surface_name, path):
#     content = readFile(file_name)
#     job_name = os.getcwd().split('/')[-1] +'/'+ path.split('/')[-1]
#     new_line = '#PBS -N ' + job_name + '\n'
#     with open(path + '/run.sh', 'w') as modified:
#         content.insert(1,new_line)
#         content = ''.join(content)
#         modified.write(content)

# def new_trajectory_name(path):
#     max_traj = 0
#     for file in os.listdir(path):
#         if file.startswith('opt') and file.endswith('traj'):
#             # opt_traj_list.append(file)
#             if file[3] != '.':
#                 curr_traj = int(file[3])
#                 if curr_traj >= max_traj:
#                     max_traj = curr_traj
#     new_traj = ' \'opt'+str(max_traj+1)+'.traj\''
#     new_traj_line = 'traj_file = '+ new_traj
#     return new_traj_line

# def generate_run_py(file_name, surface_name, path):
#     content = readFile(file_name)
#     if 'O2' in surface_name:
#         content[11] = '#'+content[11]
#         content[10] = '#'+content[10]
#     new_line = 'image = read(\'' + surface_name + '\')\n'
#     if 'converged.traj' in os.listdir(path):
#         new_line = 'image = read(\'' + 'converged.traj' + '\')\n'
#     else:
#         for file in os.listdir(path):
#             if file.startswith('opt') and file.endswith('traj'):
#                 # print(file)
#                 new_line = 'image = read(\'' + file + '\')\n' 
#                 break
#     print(path, new_line)
#     new_traj_line = new_trajectory_name(path)
#     print(path, new_traj_line)
#     with open(path + '/run.py', 'w') as modified:
#         content.insert(6,new_line)
#         content.insert(18,new_traj_line)
#         content = ''.join(content)
#         modified.write(content)
     
# def copy_script(file_name, dir):
#     cur_dir = os.getcwd()
#     for child in os.listdir(dir):
#         path = os.path.join(dir, child)
#         if os.path.isdir(path):
#             surface_name = str(child) +'.traj'
#             # if not file_name in os.listdir(path):
#             if file_name == 'run.sh':
#                 generate_run_sh(file_name, surface_name, path)
#             elif file_name == 'run.py':
#                 generate_run_py(file_name, surface_name, path)
#             elif file_name == 'parameters.json':
#                 generate_parameters(file_name, surface_name, cur_dir, path)
#     print('File generation completed!')


# copy_script('run.sh', 'ads_slab')
# copy_script('run.py', 'ads_slab')
# copy_script('parameters.json', 'ads_slab')

# copy_script('run.sh', 'slab')
# copy_script('run.py', 'slab')
# copy_script('parameters.json', 'slab')

           
 