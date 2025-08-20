import os
from shutil import copy, move
import numpy as np
import matplotlib.pyplot as plt

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

cur_dir = os.getcwd()
def get_eng_matrix(cur_dir):
    f_list = []
    h_list = []
    k_list = []
    eng_list = []
    for child in os.listdir(cur_dir):
        path = os.path.join(cur_dir, child)
        if os.path.isdir(path) and 'k' in child and 'C' not in child and 'c' not in child  and '9' not in child:
            print(child)
            f = child.split('_')[1]
            h = child.split('_')[3]
            k = int(child.split('_')[5])
            if k <=4:
                f_list.append(float(f))
                h_list.append(float(h))
                k_list.append(int(k))
                eng = readFile(path+'/HSE_energy.txt')[0]
                eng_list.append(float(eng))
            else: continue
    # print((f_list),(h_list),k_list)
    # eng_matrix = np.zeros((len(set(f_list)),len(set(h_list))))
    eng_matrix = np.zeros((len(set(k_list)),len(set(h_list))))
    hk = list(zip(h_list,k_list, eng_list))
    hk.sort(key = lambda x: x[1]) 
    print(hk)
    for i in range(len(eng_matrix)):
        for j in range(len(eng_matrix[0])):
            eng_matrix[i,j] = hk[j+i*len(eng_matrix[0])][2]
    f_val = sorted(set(f_list))
    h_val = sorted(set(h_list))
    k_val = sorted(set(k_list))
    return eng_matrix, f_val, h_val,k_val
CH3N2 = 'ads_slab/CH3N2_c'
N2_rutile_110 = 'ads_slab/N2_rutile_110'
slab = 'slab/rutile_O_br_vacant'
CH3OH = '../HSE_ref/reference/CH3OH'
N2 = '../HSE_ref/reference/N2'
O2 =  '../HSE_ref/reference/O2'
H2 = '../HSE_ref/reference/H2'
H2O = '../HSE_ref/reference/H2O'

CH3N2_eng, f_val, h_val,k_val = get_eng_matrix(CH3N2)
# print(CH3N2_eng)
N2_rutile_110_eng, f_val, h_val,k_val = get_eng_matrix(N2_rutile_110)
slab_eng, f_val, h_val,k_val = get_eng_matrix(slab)#[0]
# print(slab_eng)
CH3OH_eng, f_val, h_val,k_val = get_eng_matrix(CH3OH)#[0]
CH3OH_eng=np.repeat(CH3OH_eng,3,axis = 0)

N2_eng, f_val, h_val,k_val = get_eng_matrix(N2)#[0]
print(N2_eng)
N2_eng=np.repeat(N2_eng,3,axis = 0)
print(N2_eng)

H2_eng, f_val, h_val,k_val = get_eng_matrix(H2)#[0]
H2_eng=np.repeat(H2_eng,3,axis = 0)

H2O_eng, f_val, h_val,k_val = get_eng_matrix(H2O)#[0]
H2O_eng=np.repeat(H2O_eng,3,axis = 0)

H_eng = 0.5*H2_eng
O_eng = H2O_eng - H2_eng
C_eng = CH3OH_eng - O_eng - 4* H_eng

print('CH3N2_slab:','\n',CH3N2_eng)
print('N2_slab:','\n',N2_rutile_110_eng)
print('slab:','\n',slab_eng)

CH3N2_eng_matrix = CH3N2_eng - slab_eng - N2_eng - C_eng - 3*H_eng
print('CH3N2 adsorption energy:', '\n',CH3N2_eng_matrix)

N2_rutile_110_eng_matrix = N2_rutile_110_eng - slab_eng - N2_eng 
print('N2 adsorption energy:', '\n',N2_rutile_110_eng_matrix)

CH3N2_ref = -(- N2_eng - C_eng - 3*H_eng)
print('CH3N2 calculated reference energy:', '\n',CH3N2_ref)

# CH3N2_ref = -(- N2_eng - C_eng - 3*H_eng)
print('N2 reference energy:', '\n',N2_eng)

CH3N2_ads = float(readFile('ads_slab/CH3N2_c/HSE_energy.txt')[0])
# N2_ads = float(readFile('ads_slab/CH3N2_c/f_5e-05_h_0.079_k_4/HSE_energy.txt')[0])
SLAB = float(readFile('slab/rutile_O_br_vacant/HSE_energy.txt')[0])

print(CH3N2_ads - SLAB - CH3N2_ref[-1][-1])

# print(f_val, h_val)
# #plot eng_dff vs h; f constant

# eng_diff_h = []
# for row in eng_matrix:
#     diff=[]
#     finest_eng = row[0]
#     for i in row:
#         diff.append(np.abs(i-finest_eng))
#     eng_diff_h.append(diff)
# eng_diff_h=np.array(eng_diff_h)+1e-100
# eng_diff_h=np.sort(eng_diff_h)

# print(eng_diff_h)
# print(np.sort(eng_diff_h))
# eng_diff_f = []
# for row in eng_matrix.T:
#     diff=[]
#     finest_eng = row[0]
#     print(finest_eng)
#     for i in row:
#         diff.append(np.abs(i-finest_eng))
#     eng_diff_f.append(diff)
# eng_diff_f=np.array(eng_diff_f)+1e-100
# print(eng_diff_f)

# fig, ax = plt.subplots(2,2, figsize=(14,10))

# for i,f in enumerate(f_val):

#     ax[i%2,i//2].set_xlabel('h')
#     # ax[i%2,i//2].set_ylabel('(Eng_diff)')
#     # ax[i%2,i//2].plot(h_val,(eng_diff_h)[i],'.-',label='tol_fock='+str(f))
#     ax[i%2,i//2].plot(h_val,np.log((eng_diff_h)[i]),'.-',label='tol_fock='+str(f))
#     ax[i%2,i//2].set_ylabel('log(Eng_diff)')

#     ax[i%2,i//2].legend()
# fig.savefig('CH3N2_convergence_h.png')

# fig, ax = plt.subplots( figsize=(14,10))
# for i,f in enumerate(f_val):
#     ax.set_ylabel('(Eng_diff)')
#     ax.plot(h_val,(eng_diff_h)[i],'.-',label='tol_fock='+str(f))
#     ax.set_xlabel('h')
#     # ax.set_ylim(-10,0)
#     ax.legend()
# fig.savefig('CH3N2_convergence_h_abs.png')

# fig, ax = plt.subplots( figsize=(14,10))
# for i,f in enumerate(f_val):

#     ax.plot(h_val,np.log((eng_diff_h)[i]),'.-',label='tol_fock='+str(f))
#     ax.set_ylabel('log(Eng_diff)')
#     ax.set_xlabel('h')
#     ax.set_ylim(-10,0) 
#     ax.legend()
# fig.savefig('CH3N2_convergence_h_log.png')

# fig, ax = plt.subplots(2,2, figsize=(14,10))
# for i,h in enumerate(h_val):

#     ax[i%2,i//2].set_xlabel('f')
#     # ax[i%2,i//2].set_ylabel('Eng_diff')
#     # ax[i%2,i//2].plot(f_val,(eng_diff_f)[i],'.-',label='h='+str(h))
#     ax[i%2,i//2].plot(f_val,np.log((eng_diff_f)[i]),'.-',label='h='+str(h))
#     ax[i%2,i//2].set_ylabel('log(Eng_diff)')

#     ax[i%2,i//2].legend()
# fig.savefig('CH3N2_convergence_f.png')

CH3N2 = 'ads_slab/CH3N2_c'
slab = 'slab/rutile_O_br_vacant'
CH3OH = 'reference/CH3OH'
N2 = 'reference/N2'
O2 =  'reference/O2'
H2 = 'reference/H2'
H2O = 'reference/H2O'

# cur_dir = os.getcwd()
def get_eng_dict(cur_dir):
    f_list = []
    h_list = []
    k_list = []
    eng_list = []
    eng_dict = {}
    eng_matrix = np.zeros((3,1))
    counter = 0
    for child in os.listdir(cur_dir):
        path = os.path.join(cur_dir, child)
        # if child == 'f_5e-05_h_0.1':
        #     eng = readFile(path+'/HSE_energy.txt')[0]
        #     eng_matrix[0] = eng
        if os.path.isdir(path) and 'k' in child:
            f = child.split('_')[1]
            h = child.split('_')[3]
            k = child.split('_')[5]
            if k == str(1) and h == str(0.1) and 'reference' in cur_dir:
                eng = readFile(path+'/HSE_energy.txt')[0]
                eng_matrix[0] = eng
                eng_matrix[1] = eng
                eng_matrix[2] = eng
            elif k == str(1) and h == str(0.1):
                eng = readFile(path+'/HSE_energy.txt')[0]
                eng_matrix[0] = eng
            elif k == str(2) and h == str(0.1):
                eng = readFile(path+'/HSE_energy.txt')[0]
                eng_matrix[1] = eng
            elif k == str(4) and h == str(0.1):
                eng = readFile(path+'/HSE_energy.txt')[0]
                eng_matrix[2] = eng
            # elif k == str(1) and h == str(0.1):
            #     eng = readFile(path+'/HSE_energy.txt')[0]
            #     eng_matrix[0] = eng
            #     eng_matrix[1] = eng
            #     eng_matrix[2] = eng

            # print(h,k)
            # try:
            #     eng = readFile(path+'/HSE_energy.txt')[0]
            #     # print(eng)
                
            #     eng_matrix[counter//2,counter%2] = eng
            #     # eng_list.append(float(eng))
            #     counter+= 1
            # except:
            #     counter+= 1
            #     continue
    return eng_matrix
# CH3N2_eng=(get_eng_dict(CH3N2))
# # print(CH3N2_eng)
# slab_eng=get_eng_dict(slab)
# CH3OH_eng=get_eng_dict(CH3OH)
# H2_eng=get_eng_dict(H2)
# N2_eng=get_eng_dict(N2)
# H2O_eng=get_eng_dict(H2O)
# H_eng = 0.5*H2_eng
# N_eng = 0.5*N2_eng
# O_eng = H2O_eng - H2_eng
# C_eng = CH3OH_eng - O_eng - 4* H_eng
# # print(C_eng)
# # print(H_eng)
# # print(N_eng)
# # print(O_eng)
# eng_matrix = CH3N2_eng - slab_eng - N2_eng - C_eng - 3*H_eng
# print(eng_matrix)

# fig, ax = plt.subplots( figsize=(14,10))
# ax.set_ylabel('E_ads (eV)')
# ax.plot([1,2,4],eng_matrix,'.-',label='tol_fock='+str(5e-5)+', h = 0.1 A')
# ax.set_xlabel('kpt')
# ax.set_title('E_ads vs kpt')
# # ax.set_ylim(-10,0)
# ax.legend()
# fig.savefig('CH3N2_convergence_k_ads.png')

