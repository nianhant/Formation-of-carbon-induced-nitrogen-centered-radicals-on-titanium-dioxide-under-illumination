import os
import dft_energy_pull
from ase.io import read
import numpy as np
from ase.thermochemistry import *
from ase.build import molecule
CH3NH2 = '/storage/home/hcoda1/3/ntian30/research/carbon/02Aug_vib_paired/reference/CH3NH2/converged.traj'
CH3NH2 = read(CH3NH2)
CH3NH2 = CH3NH2.copy()

form_dict = {'N2':{'atoms':molecule('N2'),'geometry':'linear','natoms':2,'symmetrynumber':2,'spin':0},
             'CH3':{'atoms':molecule('CH3'),'geometry':'nonlinear','natoms':4,'symmetrynumber':3,'spin':0.5},
             'NH3':{'atoms':molecule('NH3'),'geometry':'nonlinear','natoms':4,'symmetrynumber':3,'spin':0},
             'H2':{'atoms':molecule('H2'),'geometry':'linear','natoms':2,'symmetrynumber':2,'spin':0},
             'CH3NH2':{'atoms':CH3NH2,'geometry':'nonlinear','natoms':7,'symmetrynumber':1,'spin':0.5}}
P_H2 = 1 # atm
P_N2 = 0.8 # atm
P_CH3 = 1 # atom
P_CH3NH2 = 1 # atom
pressure_dict = {'H2': P_H2*101325,
                 'N2': P_N2*101325,
                'CH3': P_CH3*101325,
                'NH3': P_CH3*101325,
                'CH3NH2': P_CH3NH2*101325}
temp = 300#K
pressure = 101325

def readFile(path):
    f = open(path, 'r')
    content = f.readlines()
    return content

################ Reference #################
def ref_parse_vib_eng(root):
    f = open(root + '/vib.txt')
    raw = f.read().splitlines()
    f.close()
    vib_eng = [] #meV out of the file, converted to eV below
    vib_freq = [] #cm^-1
    for line in raw:
        if '-' not in line and 'eV' not in line:
            d = line.strip()
            d,freq = d.rsplit(' ',1)
            try:
                vib_freq.append(float(freq))
                d = d.strip()
                d,eng = d.rsplit(' ',1)
                vib_eng.append(float(eng)/10**3) #converting to eV
            except:
                continue
    return vib_eng, vib_freq
           
######################### vibration data for reference ############################
def ref_vib(path):
    cur_dir = os.path.realpath(path)
    ref_vib_dict = {}
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'vib.txt' in files:
            vib_eng, vib_freq = ref_parse_vib_eng(root)
            ref_name = root.split('/')[-1]
            if ref_name not in ref_vib_dict:
                ref_vib_dict[ref_name] = {}
            ref_vib_dict[ref_name]['vib_eng'] = vib_eng
            ref_vib_dict[ref_name]['vib_freq'] = vib_freq
    return ref_vib_dict

######################### vibration eng -> Gibbs energy for reference ############################
def ref_vib_eng(path):
    vib_dict = ref_vib(path)
    ref_free_eng = {}
    for formula in vib_dict.keys():
        vibration_list = vib_dict[formula]
        vib_eng = vibration_list['vib_eng'][:]
        vib_eng.sort(reverse=True)
        if formula in form_dict.keys():
            num_atom = form_dict[formula]['natoms']
            geo = form_dict[formula]['geometry']
            if geo =='linear':
                dof = 3 * num_atom - 5
            else:
                dof = 3 * num_atom - 6
            vib_eng =  vib_eng[:dof]
            pressure = pressure_dict[formula]
            vib_thermo = IdealGasThermo(vib_energies=vib_eng,**form_dict[formula])
            ref_free_eng[formula] = vib_thermo.get_gibbs_energy(temp,pressure,verbose=False)
    return ref_free_eng

######################### add vibration energy to electronic energy for reference ############################

# Grab each ads from ads_slab and calculate respective energy
def update_reference_eng(reference, ads_slab):
    reference['H'] = 0.5*reference['H2']
    reference['N'] = 0.5*reference['N2']
    for ads, e in ads_slab.items():
        if ads == 'CH3':
            continue
        ads = ads[3:]
        e_tot = 0
        i = 0
        while i < len(ads):
            try:
                e_tot += reference[ads[i]]
            except:
                e_tot += (int(ads[i])-1)*reference[ads[i-1]]
            i+= 1
        reference['CH3'+ads] = e_tot
    return reference

def ref_eng_add_vib_eng(ele_path, vib_path):
    adsorbates = dft_energy_pull.ads_slab_eng(ele_path)
    ref_eng = dft_energy_pull.reference_eng(ele_path)
    ref_vibration_energy = ref_vib_eng(vib_path + '/reference')
    for key in ref_vibration_energy:
        if key in ref_eng:
            ref_eng[key] += ref_vibration_energy[key]
    ref_eng = update_reference_eng(ref_eng, adsorbates)
    return ref_eng

################ Ads + Slab #################
def ads_slab_parse_vib_eng(root):
    f = open(root + '/vib.txt')
    raw = f.read().splitlines()
    f.close()
    vib_eng = [] #meV out of the file, converted to eV below
    vib_freq = [] #cm^-1
    for line in raw:
        if '-' not in line and 'eV' not in line:
            d = line.strip()
            d,freq = d.rsplit(' ',1)
            try:
                vib_freq.append(float(freq))
                d = d.strip()
                d,eng = d.rsplit(' ',1)
                vib_eng.append(float(eng)/10**3) #converting to eV
            except:
                vib_eng.append(30/8065.54429)
                vib_freq.append('insert_3kT')
    return vib_eng, vib_freq

# grab the lowest energy if more than 1 present
def dict_cleanup(ads_slab_dict):
    new_dict = {}
    for surf in ads_slab_dict:
        eng_dict = ads_slab_dict[surf]
        lowest_eng_index = min(eng_dict, key=eng_dict.get)
        new_dict[surf] = eng_dict[lowest_eng_index]
    return new_dict
    
def ads_slab_vib(path):
    cur_dir = os.path.realpath(path)
    ads_slab_vib_dict = {}
    for root, dirs, files in os.walk(cur_dir, topdown=True):
        files = set(files)
        if 'vib.txt' in files:
            vib_eng, vib_freq = ads_slab_parse_vib_eng(root)
            ads_name = root.split('/')[-1]
            ads_name = ads_name.split('_')[-2]
            if ads_name not in ads_slab_vib_dict:
                ads_slab_vib_dict[ads_name] = {}
            ads_slab_vib_dict[ads_name]['vib_eng'] = vib_eng
            ads_slab_vib_dict[ads_name]['vib_freq'] = vib_freq
    return ads_slab_vib_dict

def ads_slab_vib_eng(path):
    vib_dict = ads_slab_vib(path)
    ads_slab_free_eng = {}
    for formula in vib_dict.keys():
        vibration_list = vib_dict[formula]
        vib_eng = vibration_list['vib_eng'][:]
        vib_thermo = HarmonicThermo(vib_energies=vib_eng)
        ads_slab_free_eng[formula] = vib_thermo.get_helmholtz_energy(temp,verbose=False)
    return ads_slab_free_eng

def ads_slab_add_vib_eng(ele_path, vib_path):
    ads_slab_energy = dft_energy_pull.ads_slab_eng(ele_path)
    ads_slab_energy = dict_cleanup(ads_slab_energy)
    ads_slab_vibration_energy = ads_slab_vib_eng(vib_path + '/ads_slab')
    for key in ads_slab_vibration_energy:
        if key in ads_slab_energy:
            ads_slab_energy[key] += ads_slab_vibration_energy[key]
    return ads_slab_energy
    
 

