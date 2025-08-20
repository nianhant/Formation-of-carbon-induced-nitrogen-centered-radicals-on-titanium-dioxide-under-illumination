import os
from shutil import copy, move
import numpy as np
import matplotlib.pyplot as plt

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

cur_dir = os.getcwd()
f_list = []
h_list = []
eng_list = []
for child in os.listdir(cur_dir):
    path = os.path.join(cur_dir, child)
    if os.path.isdir(path):
        f = child.split('_')[1]
        h = child.split('_')[3]
        f_list.append(float(f))
        h_list.append(float(h))
        eng = readFile(path+'/HSE_energy.txt')[0]
        eng_list.append(float(eng))
eng_matrix = np.zeros((len(set(f_list)),len(set(h_list))))
for i in range(len(eng_matrix)):
    for j in range(len(eng_matrix[0])):
        # print(j+i*len(eng_matrix[0]))
        # print(eng_list[j+i*len(eng_matrix[0])])
        eng_matrix[i,j] = eng_list[j+i*len(eng_matrix[0])]

f_val = sorted(set(f_list))
h_val = sorted(set(h_list))
print(f_val, h_val)
# plot eng_dff vs h; f constant
eng_diff_h = []
for row in eng_matrix:
    diff=[]
    finest_eng = row[0]
    for i in row:
        diff.append(np.abs(i-finest_eng))
    eng_diff_h.append(diff)
eng_diff_h=np.array(eng_diff_h)+1e-100
# print(eng_diff_h)

eng_diff_f = []
for row in eng_matrix.T:
    diff=[]
    finest_eng = row[0]
    for i in row:
        diff.append(np.abs(i-finest_eng))
    eng_diff_f.append(diff)
eng_diff_f=np.array(eng_diff_f)+1e-100
# print(eng_diff_f)

# fig, ax = plt.subplots(2,2, figsize=(14,10))
# for i,f in enumerate(f_val):
#     # ax[i%2,i//2].plot(h_val,np.log((eng_diff_h)[i]),'.-',label='tol_fock='+str(f))
#     ax[i%2,i//2].plot(h_val,(eng_diff_h)[i],'.-',label='tol_fock='+str(f))
#     ax[i%2,i//2].set_xlabel('h')
#     # ax[i%2,i//2].set_ylabel('log(Eng_diff)')
#     ax[i%2,i//2].set_ylabel('(Eng_diff)')
#     ax[i%2,i//2].legend()
# fig.savefig('CH3N2_convergence_h.png')

# fig, ax = plt.subplots(2,2, figsize=(14,10))
# for i,h in enumerate(h_val):
#     # ax[i%2,i//2].plot(f_val,np.log((eng_diff_f)[i]),'.-',label='h='+str(h))
#     ax[i%2,i//2].plot(f_val,(eng_diff_f)[i],'.-',label='h='+str(h))
#     ax[i%2,i//2].set_xlabel('f')
#     ax[i%2,i//2].set_ylabel('Eng_diff')
#     # ax[i%2,i//2].set_ylabel('log(Eng_diff)')
#     ax[i%2,i//2].legend()
# fig.savefig('CH3N2_convergence_f.png')
