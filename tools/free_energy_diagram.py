from vib_pull import *
from dft_energy_pull import *
from catmap.analyze import MechanismPlot
from pylab import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def absolute_free_energy(ele_path, vib_path):
    ele_path = '../'+ ele_path
    vib_path = '../'+ vib_path
    ref_absolute_free_energy = ref_eng_add_vib_eng(ele_path, vib_path)
    print(ref_absolute_free_energy)
    ads_slab_absolute_free_energy = ads_slab_add_vib_eng(ele_path, vib_path)
    slb_free_energy = slab_eng(ele_path)
    absolute_free_eng = {}
    absolute_free_eng['CH3'] =  (ads_slab_absolute_free_energy['CH3']# + ref_absolute_free_energy['N2'])
                                  - ref_absolute_free_energy['CH3']) 
                                #  - slb_free_energy['rutile_O_br_vacant'] )
    for ads in ads_slab_absolute_free_energy:
        if ads == 'CH3': 
            continue
        absolute_free_eng[ads] = (ads_slab_absolute_free_energy[ads] - ref_absolute_free_energy[ads] )
                                 #- slb_free_energy['rutile_O_br_vacant'])#- absolute_free_eng['CH3'])# - ref_absolute_free_energy['CH3'])#- slb_free_energy['rutile_O_br_vacant']) 
        # if ads == 'CH3': 
        #     absolute_free_eng[ads] += ref_absolute_free_energy['CH3']
    absolute_free_eng['N2'] = ref_absolute_free_energy['N2']
    absolute_free_eng['CH3_2NH3'] = absolute_free_eng['CH3'] - ref_absolute_free_energy['N2'] + 2*ref_absolute_free_energy['NH3']
    return absolute_free_eng

# free_energy_dict = absolute_free_energy('02Aug_spin_polarized', '02Aug_vib_paired')
# print(free_energy_dict)
 
potential_step = ['CH3','CH3N2','CH3N2H', 'CH3NNHH','CH3NNHHH','CH3NNH3', 'CH3N','CH3NH','CH3NHH']

def generate_eng_list(absolute_free_eng):
    eng = []
    for reliable_ads in potential_step:
        print(reliable_ads, ':', absolute_free_eng[reliable_ads], 'eV')
        eng.append(absolute_free_eng[reliable_ads])
    print('==========================')
    return eng
# eng_list = generate_eng_list(free_energy_dict)
# print(eng_list)

def FED_plot(eng_list):
    states = ['CH3*+N2 ','CH3N2*','CH3N2H*', 'CH3NNHH*','CH3NNHHH*','CH3N*+NH3', 'CH3N*','CH3NH*','CH3NHH*']#,'CH3*+NH3']
    rxn = MechanismPlot(energies=eng_list,labels=states)
    rxn.barriers = [-207]*8
    rxn.initial_energy = eng_list[0]
    rxn.energy_mode = "absolute"

    rxn.label_args['color'] = 'b'
    rxn.label_args['size'] = 10
    rxn.label_args['rotation'] = 10
    rxn.barrier_line_args['color'] = 'r'

    figsize_dict = {'figsize':(8, 6)}
    fig = plt.figure(**figsize_dict)
    ax = fig.add_subplot(111)
    rxn.draw(ax)
    # print()
    plt.xlabel('Reaction Coordinate')
    plt.ylabel('State Free Energy (eV)')
    plt.title('Free Energy Diagram')
    # potential= -0.
    # textstr='potential='+str(potential )+'V\n'#+'References:\n'
    
    props = dict(facecolor='white', alpha=0.5)
    # ax.text(0.05, 0.08, textstr, transform=ax.transAxes, fontsize=14,
    #     verticalalignment='top')
    ya = ax.get_yaxis()
    ya.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    fig.savefig('FED1.png')

# FED_plot(eng_list)


########################################################
def test(path):
    path = '../'+ path
    # answer = ads_slab_eng(path)
    answer = ads_slab_vib_eng(path+'/ads_slab')
    # answer = ref_eng_add_vib_eng('../02Aug_spin_polarized', path)
    # print(answer)
    # for reliable_ads in ƒ:
    print('CH3NH', ':', answer['CH3NH'], 'eV')
    print('CH3NHH', ':', answer['CH3NHH'], 'eV')
        # eng.append(absolute_free_eng[reliable_ads])
    print('==========================')
    # return engs
# test('1Jul_vib')
# test('1Jul_vib') '1Jul_vib' is broken
# test('02Aug_vib_paired')
# test('28Jul_calc')
# test('02Aug_spin_polarized')
# test('26Jul_spin_polarized')
###### '02Aug_spin_polarized' -> lowest energies

def rxn_energy(rxn_states, initial_state, energy_dict,initial_zero=True):
    rxn_states = [s for s in rxn_states] #make a copy
    initial_state = [[s for s in initial_state]] #make a copy
    E_p1 = []
    if initial_zero == True:
        sts = initial_state+rxn_states
    else:
        sts = rxn_states
    for state in initial_state+rxn_states:
        for i, sp in enumerate(state): #pull off the multiplication
            if '*' in sp:
                n,s = sp.split('*')
                n = float(n)
            else:
                n = 1
                s = sp
            state[i] = [n,s]
    for i,state in enumerate(sts):
        # print(i, state)
        # print(E_p1)
        E_p1.append(sum([d*energy_dict[p] for d,p in (sts)[i]]))
    E_r1 = sum([s*energy_dict[r] for s,r in initial_state[0]])
    if initial_zero==True:
        dE1 = E_p1-E_r1
    else:
        dE1 = E_p1
    state_energy = dE1
    return state_energy

rxn_states = ['CH3N2',
              'CH3N2H', 
              'CH3NNHH',
              'CH3NNHHH',
              'CH3NNH3', 
              'CH3N',
              'CH3NH',
              'CH3NHH']
r_s = []
for i in rxn_states:
    r_s.append([i])

# print(r_s)
# initial_state = ['CH3','N2']
# energy_dict = free_energy_dict
# print(rxn_energy(r_s, initial_state, energy_dict,initial_zero=True))