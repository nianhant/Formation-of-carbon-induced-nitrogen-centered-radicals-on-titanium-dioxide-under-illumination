import os
# import pathlib
from shutil import copy, move,rmtree

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content
 
# tol_fock_list = [1e-5, 5e-5, 1e-4,3e-4]
# h_list = [0.15, 0.175, 0.2, 0.25]
tol_fock_list = [5e-5]
# h_list = [0.079, 0.092, 0.105, 0.132]
# h_list = [0.05,0.1]
h_list = [0.075,0.1]
# k_list = [[2,2,1], [4,4,1]]
k_list = [[1,1,1]]

def copy_files(tol_fock_list,h_list,k_list,path):
    for f in tol_fock_list:
        for h_val in h_list:
            for k in k_list:
                # make a new directory
                new_dir = path + '/f_'+str(f)+'_h_'+ str(h_val) +'_k_'+ str(k[0])
                # if not os.path.exists(new_dir):
                #     os.makedirs(new_dir)
                if os.path.exists(new_dir):
                    rmtree(new_dir) 
                os.makedirs(new_dir)
                # copy traj, energy.txt, run.sh to that directory
                copy(path+'/run.sh', new_dir)
                copy(path+'/converged.traj', new_dir)

                # modify and copy new run.py to that directory
                content = readFile(path+'/run.py')
                new_line='             TOL_FOCK='+str(f)+', h = '+str(h_val) + ', KPOINT_GRID = ' + str(k) + ',\n'
                content[22] = new_line
                print(new_dir)
                with open(new_dir + '/run.py', 'w') as modified:
                    content = ''.join(content)
                    modified.write(content)

cur_dir = os.getcwd()
for child in os.listdir(cur_dir):
    path = os.path.join(cur_dir, child)
    if os.path.isdir(path):
        print(path)
        copy_files(tol_fock_list,h_list,k_list,path)