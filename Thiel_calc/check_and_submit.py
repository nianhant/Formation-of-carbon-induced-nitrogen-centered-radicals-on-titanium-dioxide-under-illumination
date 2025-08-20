import os
import sys
import json
from subprocess import call
from subprocess import run
import re
# call make_directory first
call(["python","make_directory.py"])

# parse stdout
def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

# find Job ID
def parse_stdout(root):
    f = open(root + '/stdout')
    raw = f.read() 
    job_id = re.findall(r'(?<=Job ID:     )[\d]+', raw)
    # print(job_id)
    return set(job_id)
    

# check if no 'converged.traj', check status
# if stat is R: do nothing
# elif stat is C: resubmit
def get_status(job_id):
    cmd = ['qstat -f {} | grep "job_state = "'.format(job_id)]
    output = run(cmd, shell = True, capture_output=True).stdout
    status = re.findall(r'(?<=job_state = )[A-Z]', output.decode('utf-8'))#[0]
    # print(status)
    return status#[0]


def generate_run_py(file_name, surface_name, path):
    content = readFile(file_name)
    content[6] = 'image = read(\'' + surface_name +'.traj' + '\')\n'
    # print(content[6])
    with open('run.py', 'w') as modified:
        content[6] = 'image = read(\'' + surface_name +'.traj' + '\')\n'
        content = ''.join(content)
        # print(content[6])
        modified.write(content)
        
# run_py_file_name = 'ads_slab/CH3OH_a/run.py'
# generate_run_py(run_py_file_name, 'H2O_a', 'ads_slab/H2O_a')

def submit(dir):
    cur_dir=os.path.realpath('.')
    for root, dirs, files in os.walk(dir, topdown=False):
        files = set(files)
        if 'converged.traj' not in files:
            if 'run.sh' in files:
                try:
                    # 1) the job was failed before
                    job_id = parse_stdout(root)
                    status_list = [get_status(id) for id in job_id]
                    os.chdir(os.path.join(root))
                    # print(status_list)
                    if (['C'] in status_list or [] in status_list) and (['R'] not in status_list):
                        run_py_file_name = 'run.py'
                        surface_name = root.split('/')[-1]
                        # generate_run_py(run_py_file_name, surface_name, os.getcwd())
                        print(status_list)
                        print('In try, should run')
                        print('run '+root)
                        call(["qsub","run.sh"])
                    os.chdir(cur_dir)
                except:
                    # break
                    # 2) the job was never submitted
                    # job_id = parse_stdout(root)
                    # print('ecept ',root, job_id)
                    # status_list = [get_status(id) for id in job_id]
                    # print(status_list)
                    os.chdir(os.path.join(root))
                    print('ecept should run')
                    print('run '+root)
                    call(["qsub","run.sh"])
                    os.chdir(cur_dir) 
submit('ads_slab')
submit('slab')










