import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-bright')

STAND_T = 298


# check equivalence of a given equilibrated value
# all should be near 0
def check_equiv(gas1):
    rf = gas1.forward_rates_of_progress
    rr = gas1.reverse_rates_of_progress
    for i in range(gas1.n_reactions):
        if gas1.is_reversible(i) and rf[i] != 0.0:
            print(' %4i  %10.4g  ' % (i, (rf[i] - rr[i]) / rf[i]))


# plot phi vs adiabatic temps
def plot_phitemps(phi, temps, title):
    plt.plot(equivs, temps, '--k')
    plt.xlabel('Phi')
    plt.ylabel('Flame Temperature (K)')
    plt.title(title)
    plt.show()


# main function
if __name__ == "__main__":
    gas1 = ct.Solution('gri30.xml')
    # generate phi values and numpy array for temps
    equivs = [x / 10 + 0.4 for x in range(22)]
    temps = np.empty(shape=(22))
    count = 0
    for phi in equivs:
        # reset composition, temp, pressure
        comp_dict = {'C3H8': 1, 'O2': 5 / phi, 'N2': 5 * 3.76 / phi}
        gas1.TPX = STAND_T, ct.one_atm, comp_dict
        # equilibrate mixture
        gas1.equilibrate('HP')
        # store equilibrated temperature (adiabat)
        temps[count] = gas1.T
        print(gas1['O2'].X)
        # increment index counter
        count += 1

    # print phi and adiabat temp values
    print(equivs)
    print(temps)

    # plot temps vs phi using matplotlib
    plot_phitemps(
        equivs, temps, 'Adiabatic Flame Temperature as a Function of Phi')
