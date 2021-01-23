import cantera as ct
import numpy as np


# main function
if __name__ == "__main__":
    gas1 = ct.Solution('gri30.xml')
    equivs = [x / 10 + 0.4 for x in range(22)]
    temps = np.empty(shape=(22))
    count = 0
    for phi in equivs:
        gas1.X = {'C2H6': 1, 'O2': 3.5 / phi, 'N2': 3.5 * 3.76 / phi}
        gas1.T = 298
        gas1.equilibrate('HP')
        temps[count] = gas1.T
        gas1()
        count += 1
    rf = gas1.forward_rates_of_progress
    rr = gas1.reverse_rates_of_progress
    for i in range(gas1.n_reactions):
        if gas1.is_reversible(i) and rf[i] != 0.0:
            print(' %4i  %10.4g  ' % (i, (rf[i] - rr[i]) / rf[i]))

    print("done")
