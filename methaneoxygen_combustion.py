import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-bright')
plt.rcParams["figure.figsize"] = (6, 4)


COMP = ['H2O', 'H2', 'O2', 'CO', 'CO2']
STAND_T = 298


# check equivalence of a given equilibrated value
# all should be near 0
def check_equiv(fuelMix):
    rf = fuelMix.forward_rates_of_progress
    rr = fuelMix.reverse_rates_of_progress
    for i in range(fuelMix.n_reactions):
        if fuelMix.is_reversible(i) and rf[i] != 0.0:
            print(' %4i  %10.4g  ' % (i, (rf[i] - rr[i]) / rf[i]))


# plot equilibrium components of the mixture (major)
def plot_components(phi_vals, comps, title):
    for i in range(len(COMP)):
        plt.plot(phi_vals, comps[:, i], label=COMP[i])
    plt.xlabel('ɸ')
    plt.ylabel('Compositions (mole fraction)')
    plt.title(title)
    plt.legend()
    plt.grid(axis='y')
    plt.show()


# plot phi vs adiabatic temps
def plot_phitemps(phi, temps, title, yaxis):
    plt.plot(equivs, temps, '--k')
    plt.xlabel('ɸ')
    plt.ylabel('Flame Temperature (K)')
    plt.title(title)
    plt.ylim(0, 3200)
    plt.grid(axis='y')
    plt.show()


# plot phi vs pressures
def plot_phipressure(phi, pressures, title, yaxis):
    plt.plot(equivs, pressures / 101325, '--k')
    plt.xlabel('ɸ')
    plt.ylabel('Combustion Pressures (atm)')
    plt.title(title)
    plt.ylim(0, 25)
    plt.grid(axis='y')
    plt.show()


# main function
if __name__ == "__main__":
    fuelMix = ct.Solution('gri30.xml')
    # generate phi values and numpy array for temps
    equivs = [x / 100 + 0.4 for x in range(211)]
    # empty arrays for temperatures
    flametemps = np.empty(shape=(211))
    combtemps = np.empty(shape=(211))
    combpress = np.empty(shape=(211))
    compflame = np.empty(shape=(211, 5))
    compcomb = np.empty(shape=(211, 5))
    count = 0
    for phi in equivs:
        #####################
        #   Flame Section   #
        #####################
        # reset composition, temp, pressure
        comp_dict = {'CH4': 1, 'O2': 2 / phi}
        fuelMix.TPX = STAND_T, ct.one_atm, comp_dict
        # equilibrate mixture
        fuelMix.equilibrate('HP')
        # store equilibrated temperature (adiabat)
        flametemps[count] = fuelMix.T
        compflame[count, :] = fuelMix[COMP].X
        # print(fuelMix['O2'].X)
        ##########################
        #   Combustion Section   #
        ##########################
        # reset composition, temp, pressure
        comp_dict = {'C3H8': 1, 'O2': 2 / phi}
        fuelMix.TPX = STAND_T, ct.one_atm, comp_dict
        # equilibrate mixture
        fuelMix.equilibrate('UV')
        # store equilibrated temperature (adiabat)
        combtemps[count] = fuelMix.T
        combpress[count] = fuelMix.P
        compcomb[count, :] = fuelMix[COMP].X
        # print(fuelMix['O2'].X)
        # increment index counter
        count += 1

    flametitle = 'Adiabatic Flame Temperature as a Function of ɸ, Me + O2'
    flameytitle = 'Flame Temperature (K)'
    # plot temps vs phi using matplotlib
    plot_phitemps(equivs, flametemps, flametitle, flameytitle)

    combtitle = 'Adiabatic Combustion Temperature as a Function of ɸ, Me + O2'
    combytitle = 'Combustion Temperature (K)'
    combptitle = 'Adiabatic Combustion Pressure as a Function of ɸ, Me + O2'
    combpytitle = 'Combustion Pressure (atm)'
    # plot temps vs phi using matplotlib
    plot_phitemps(equivs, combtemps, combtitle, combytitle)
    plot_phipressure(equivs, combpress, combptitle, combpytitle)

    plot_components(equivs, compflame,
                    'Flame Equilibrium Concentrations of Major Species wrt ɸ, Me + O2')
    plot_components(equivs, compcomb,
                    'Combustion Equilibrium Concentrations of Major Species wrt ɸ, Me + O2')
