import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-bright')
plt.rcParams["figure.figsize"] = (6, 4)

COMP = ['H2O', 'H2', 'O2', 'CO', 'CO2']
STAND_T = 298
STAND_P = ct.one_atm


# check equivalence of a given equilibrated value
# all should be near 0
def check_equiv(fuelMix):
    rf = fuelMix.forward_rates_of_progress
    rr = fuelMix.reverse_rates_of_progress
    for i in range(fuelMix.n_reactions):
        if fuelMix.is_reversible(i) and rf[i] != 0.0:
            print(' %4i  %10.4g  ' % (i, (rf[i] - rr[i]) / rf[i]))


# plot phi vs adiabatic temps
def plot_flame_tempvary(phi, tempvary, flametemps, title):
    plt.plot(tempvary, flametemps, '--k')
    plt.xlabel('Initial Temperature (K)')
    plt.ylabel('Flame Temperature (K)')
    plt.title(title + str(phi))
    plt.grid(axis='y')
    plt.show()


# plot phi vs adiabatic temps
def plot_flame_pressvary(phi, pressvary, flametemps, title):
    plt.plot(pressvary / 1000, flametemps, '--k')
    plt.xscale('log')
    plt.xlabel('Initial Pressure (kPa)')
    plt.ylabel('Flame Temperature (K)')
    plt.title(title + str(phi))
    plt.grid(axis='y')
    plt.show()


# plot phi vs pressures
def plot_comps_tempvary(phi, tempvary, comps, title):
    for i in range(len(COMP)):
        plt.plot(tempvary, comps[:, i] * 100, label=COMP[i])
    plt.xlabel('Initial Temperature (K)')
    plt.ylabel('Compositions (mol%)')
    plt.title(title + str(phi))
    plt.legend()
    plt.grid(axis='y')
    plt.show()


# plot phi vs pressures
def plot_comps_pressvary(phi, pressvary, comps, title):
    for i in range(len(COMP)):
        plt.plot(pressvary / 1000, comps[:, i] * 100, label=COMP[i])
    plt.xscale('log')
    plt.xlabel('Initial Pressure (kPa)')
    plt.ylabel('Compositions (mol%)')
    plt.title(title + str(phi))
    plt.legend()
    plt.grid(axis='y')
    plt.show()


# main function
if __name__ == "__main__":
    fuelMix = ct.Solution('gri30.xml')
    # generate phi values and numpy array for temps
    press_vary = np.array([x * (73800 / 25) + 33700 for x in range(26)])
    print(press_vary)
    temp_vary = np.array([x * (146 / 25) + 184 for x in range(26)])
    phi_vary = np.array([0.7, 1.0, 1.4])
    # empty arrays for temperatures
    flametemps = np.empty(shape=(26))
    flamecomps = np.empty(shape=(26, 5))
    for phi in phi_vary:
        count = 0
        for press in press_vary:
            # reset composition, temp, pressure
            comp_dict = {'C3H8': 1, 'O2': 5 / phi, 'N2': 5 * 3.76 / phi}
            fuelMix.TPX = STAND_T, press, comp_dict
            # equilibrate mixture
            fuelMix.equilibrate('HP')
            # store equilibrated temperature (adiabat)
            flametemps[count] = fuelMix.T
            flamecomps[count, :] = fuelMix[COMP].X
            # print(fuelMix['O2'].X)
            count += 1
        # print(flamecomps)
        # print(flametemps)
        plot_flame_pressvary(
            phi=phi, pressvary=press_vary, flametemps=flametemps,
            title='Change in Flame Temperature wrt Pressure, ɸ = '
        )
        plot_comps_pressvary(
            phi=phi, pressvary=press_vary, comps=flamecomps,
            title='Change in Species Compositions wrt Pressure, ɸ = '
        )
        count = 0
        for temp in temp_vary:
            # reset composition, temp, pressure
            comp_dict = {'C3H8': 1, 'O2': 5 / phi, 'N2': 5 * 3.76 / phi}
            fuelMix.TPX = temp, STAND_P, comp_dict
            # equilibrate mixture
            fuelMix.equilibrate('HP')
            # store equilibrated temperature (adiabat)
            flametemps[count] = fuelMix.T
            flamecomps[count, :] = fuelMix[COMP].X
            # print(fuelMix['O2'].X)
            count += 1
        # print(flamecomps)
        # print(flametemps)
        plot_flame_tempvary(
            phi=phi, tempvary=temp_vary, flametemps=flametemps,
            title='Change in Flame Temperature wrt Temperature, ɸ = '
        )
        plot_comps_tempvary(
            phi=phi, tempvary=temp_vary, comps=flamecomps,
            title='Change in Species Compositions wrt Temperature, ɸ = '
        )
