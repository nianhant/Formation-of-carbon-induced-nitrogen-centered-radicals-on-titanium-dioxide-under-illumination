import os
from ase import io
from ase.visualize import view
from ase.constraints import FixAtoms, FixedLine, FixBondLengths
from ase import Atoms
import numpy as np

from ase import *
from ase.build import surface, add_adsorbate, molecule
from ase.spacegroup import crystal
from ase.visualize import view
from ase.io.trajectory import TrajectoryReader
from ase.build.tools import sort
from ase.constraints import FixAtoms
import numpy as np
from ase.geometry.analysis import Analysis

def build_CH3OH():
    ########################## Load the converged slab ##########################

    CH3 = '../02Aug_spin_polarized/ads_slab/CH3_a/converged.traj'
    surf = io.read(CH3)
    slb = surf.copy()
    C_pos = slb.positions[47][:2].copy()
    del slb[47:51]
    # view(slb)
    met_1 = molecule('CH3OH')
    # view(met)
    adsorbate = met_1
    d_list = []
    C_pos_list = []
    ads_list = []

    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 1.2
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_1)
    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 1.2
    met_2 = molecule('CH3OH')
    met_2.rotate('z',150)
    adsorbate = met_2
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_2)
    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 1.2
    met_3 = molecule('CH3OH')
    met_3.rotate('z',90)
    adsorbate = met_3
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_3)
    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 1.2
    C_pos[1] += 0.5
    met_3 = molecule('CH3OH')
    met_3.rotate('z',270)
    adsorbate = met_3
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_3)
    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 2
    # C_pos[1] += 0.5
    met_4 = molecule('CH3OH')
    met_4.rotate('x',90)
    adsorbate = met_4
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_4)
    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 2
    C_pos[1] -= 0.5
    met_4 = molecule('CH3OH')
    met_4.rotate('x',90)
    met_4.rotate('z',90)
    adsorbate = met_4
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_4)
    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 2
    # C_pos[1] -= 0.5
    met_4 = molecule('CH3OH')
    met_4.rotate('x',90)
    met_4.rotate('z',180)
    adsorbate = met_4
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_4)

    ########################## Attach a methanol ##########################
    C_pos = C_pos.copy()
    d = 2
    C_pos[1] += 0.8
    met_4 = molecule('CH3OH')
    met_4.rotate('x',90)
    met_4.rotate('z',270)
    adsorbate = met_4
    d_list.append(d)
    C_pos_list.append(C_pos)
    ads_list.append(met_4)

    ########################## save structures ##########################
    order_list = ['a','b','c','d','e','f','g','h']
    cur_dir = os.getcwd()
    for adsorbate, d, C_pos, order in zip(ads_list, d_list, C_pos_list,order_list):
        new_slb = slb.copy()
        add_adsorbate(new_slb,adsorbate, d, position=C_pos)
    #     view(new_slb)
        dir_name = cur_dir + '/ads_slab/CH3OH_' + order 
        if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        file_name = dir_name + '/CH3OH_' + order +'.traj'
        # new_slb.write(file_name)
        print(file_name, '\ngeneration done')


############# find next letter
def find_ascii_ord(ads_name):
    dir_set = os.listdir('ads_slab')
    ord_set = set()
    for dir in dir_set:
        ads = dir.split('_')[0]
        if ads == ads_name:
            char = dir.split('_')[-1]
            order = ord(char)
            if order > 90 and order < 97:
                if 97 not in ord_set:
                    order = 97
                else: 
                    order = max(ord_set) + 1
            ord_set.add(order)
    if len(ord_set) == 0:
        return 65
    return  max(ord_set) + 1

def build_CH3OHN2_coadsorbed_e(site):
    if site == 'Ti':
        O_index = [18,19,42,43]
        d = 3.3
    elif site == 'O':
        O_index = [17,16,40,41]
        d = 2.5
    ########################## Load the converged slab ##########################
    CH3OH = 'ads_slab/CH3OH_e/converged.traj'
    surf = io.read(CH3OH)
    slb = surf.copy()
    adsorbate = molecule('N2')
    ############# build order_list #############
    order_list = []
    ascii_ord = find_ascii_ord('CH3OHN2')
    for i in range(ascii_ord,ascii_ord+len(O_index)):
        order_list.append(chr(i))
    cur_dir = os.getcwd()
    for o,order in zip(O_index,order_list):
        new_slb = slb.copy()
        if 'adsorbate_info' in slb.info:
            slb.info['adsorbate_info']['top layer atom index'] = o
        pos = slb.positions[o][:2].copy()
        if o == 43:
            pos[1] += 0.3
            pos[0] += 0.4
        add_adsorbate(new_slb,adsorbate, d, position=pos)
        dir_name = cur_dir + '/ads_slab/CH3OHN2_' + order 
        if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        file_name = dir_name + '/CH3OHN2_' + order +'.traj'
        new_slb.write(file_name)
        print(file_name, '\ngeneration done')

# build_CH3OHN2_coadsorbed_e('Ti')
# build_CH3OHN2_coadsorbed_e('O')

def build_CH3OHN2_coadsorbed_g(site):
    if site == 'Ti':
        O_index = [18,19,42,43]
        d = 3.3
    elif site == 'O':
        O_index = [17,16,40,41]
        d = 2.5
    ########################## Load the converged slab ##########################
    CH3OH = 'ads_slab/CH3OH_g/converged.traj'
    surf = io.read(CH3OH)
    slb = surf.copy()
    adsorbate = molecule('N2')
    ############# build order_list #############
    order_list = []
    ascii_ord = find_ascii_ord('CH3OHN2')
    for i in range(ascii_ord,ascii_ord+len(O_index)):
        order_list.append(chr(i))
    cur_dir = os.getcwd()
    for o,order in zip(O_index,order_list):
        new_slb = slb.copy()
        if 'adsorbate_info' in slb.info:
            slb.info['adsorbate_info']['top layer atom index'] = o
        pos = slb.positions[o][:2].copy()
        if o == 19:
            pos[1] -= 0.3
        elif o == 43:
            pos[1] += 0.3
        add_adsorbate(new_slb,adsorbate, d, position=pos)
        dir_name = cur_dir + '/ads_slab/CH3OHN2_' + order 
        if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        file_name = dir_name + '/CH3OHN2_' + order +'.traj'
        new_slb.write(file_name)
        print(file_name, '\ngeneration done')
# build_CH3OHN2_coadsorbed_g('Ti')
# build_CH3OHN2_coadsorbed_g('O')

def build_CH3OHN2_coadsorbed_d(site):
    if site == 'Ti':
        O_index = [18,19,42,43]
        d = 3.3
    elif site == 'O':
        O_index = [17,16,40,41]
        d = 2.5
    ########################## Load the converged slab ##########################
    CH3OH = 'ads_slab/CH3OH_d/converged.traj'
    surf = io.read(CH3OH)
    slb = surf.copy()
    adsorbate = molecule('N2')
    ############# build order_list #############
    order_list = []
    ascii_ord = find_ascii_ord('CH3OHN2')
    for i in range(ascii_ord,ascii_ord+len(O_index)):
        order_list.append(chr(i))
    cur_dir = os.getcwd()
    for o,order in zip(O_index,order_list):
        new_slb = slb.copy()
        if 'adsorbate_info' in slb.info:
            slb.info['adsorbate_info']['top layer atom index'] = o
        pos = slb.positions[o][:2].copy()
        if o == 19:
            pos[1] -= 0.3
        elif o == 43:
            pos[1] += 0.3
        add_adsorbate(new_slb,adsorbate, d, position=pos)
        dir_name = cur_dir + '/ads_slab/CH3OHN2_' + order 
        if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        file_name = dir_name + '/CH3OHN2_' + order +'.traj'
        new_slb.write(file_name)
        print(file_name, '\ngeneration done')
# build_CH3OHN2_coadsorbed_d('Ti')
# build_CH3OHN2_coadsorbed_d('O')


def build_CH3OHN2_coadsorbed_c(site):
    if site == 'Ti':
        O_index = [18,19,42,43]
        d = 3.3
    elif site == 'O':
        O_index = [17,16,40,41]
        d = 2.5
    ########################## Load the converged slab ##########################
    CH3OH = 'ads_slab/CH3OH_c/converged.traj'
    surf = io.read(CH3OH)
    slb = surf.copy()
    adsorbate = molecule('N2')
    ############# build order_list #############
    order_list = []
    ascii_ord = find_ascii_ord('CH3OHN2')
    for i in range(len(O_index)):
        i += ascii_ord
        if i > 90:
            i += 6
        order_list.append(chr(i))
    # print(order_list)
    cur_dir = os.getcwd()
    for o,order in zip(O_index,order_list):
        new_slb = slb.copy()
        if 'adsorbate_info' in slb.info:
            slb.info['adsorbate_info']['top layer atom index'] = o
        pos = slb.positions[o][:2].copy()
        if o == 19:
            pos[1] -= 0.3
        elif o == 43:
            pos[1] += 0.3
        elif o == 41:
            pos[1] -= 1.3
            d += 0.3
        add_adsorbate(new_slb,adsorbate, d, position=pos)
        dir_name = cur_dir + '/ads_slab/CH3OHN2_' + order 
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = dir_name + '/CH3OHN2_' + order +'.traj'
        new_slb.write(file_name)
        print(file_name, '\ngeneration done')
# build_CH3OHN2_coadsorbed_c('Ti')
# build_CH3OHN2_coadsorbed_c('O')

def build_CH3OHN2_coadsorbed_f(site):
    if site == 'Ti':
        O_index = [18,42,43]
        d = 3.3
    elif site == 'O':
        O_index = [17,16,40,41]
        d = 2.5
    ########################## Load the converged slab ##########################
    CH3OH = 'ads_slab/CH3OH_f/converged.traj'
    surf = io.read(CH3OH)
    slb = surf.copy()
    adsorbate = molecule('N2')
    ############# build order_list #############
    order_list = []
    ascii_ord = find_ascii_ord('CH3OHN2')
    for i in range(len(O_index)):
        i += ascii_ord
        # if i > 90:
        #     i += 6
        order_list.append(chr(i))
    # print(ascii_ord)
    # print(order_list)
    cur_dir = os.getcwd()
    for o,order in zip(O_index,order_list):
        new_slb = slb.copy()
        if 'adsorbate_info' in slb.info:
            slb.info['adsorbate_info']['top layer atom index'] = o
        pos = slb.positions[o][:2].copy()
        if o == 19:
            pos[1] -= 0.3
        elif o == 43:
            pos[1] += 0.3
        add_adsorbate(new_slb,adsorbate, d, position=pos)
        dir_name = cur_dir + '/ads_slab/CH3OHN2_' + order 
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = dir_name + '/CH3OHN2_' + order +'.traj'
        new_slb.write(file_name)
        print(file_name, '\ngeneration done')
# build_CH3OHN2_coadsorbed_f('Ti')
# build_CH3OHN2_coadsorbed_f('O')

def build_CH3OHN2_coadsorbed_h(site):
    if site == 'Ti':
        O_index = [18,19,42,43]
        d = 3.3
    elif site == 'O':
        O_index = [17,16,40,41]
        d = 2.5
    ########################## Load the converged slab ##########################
    CH3OH = 'ads_slab/CH3OH_h/converged.traj'
    surf = io.read(CH3OH)
    slb = surf.copy()
    adsorbate = molecule('N2')
    ############# build order_list #############
    order_list = []
    ascii_ord = find_ascii_ord('CH3OHN2')
    for i in range(len(O_index)):
        i += ascii_ord
        if i > 122:
            i = 48
        order_list.append(chr(i))
    # print(ascii_ord)
    # print(order_list)
    cur_dir = os.getcwd()
    for o,order in zip(O_index,order_list):
        new_slb = slb.copy()
        if 'adsorbate_info' in slb.info:
            slb.info['adsorbate_info']['top layer atom index'] = o
        pos = slb.positions[o][:2].copy()
        if o == 19:
            pos[1] -= 0.1
            pos[0] += 0.3
        elif o == 43:
            pos[1] += 0.5
        add_adsorbate(new_slb,adsorbate, d, position=pos)
        dir_name = cur_dir + '/ads_slab/CH3OHN2_' + order 
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = dir_name + '/CH3OHN2_' + order +'.traj'
        new_slb.write(file_name)
        print(file_name, '\ngeneration done')
# build_CH3OHN2_coadsorbed_h('Ti')
build_CH3OHN2_coadsorbed_h('O')