import data_reader as DATA
import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
"""
This file is the main file that will run the data analysis.
"""

#Afstanden ballonen:
D_lucht = 21.7 # pm 0.5, ballon gevuld met lucht
D_He_zwak = 23.4 # pm 0.5, ballon gevuld met commerciële Helium
D_He_sterk = 23.1 # pm 0.5, ballon gevuld met puur Helium (thx departement)

lamp1 = Lamp(1, 10)
lamp2 = Lamp(2, 5)
lamp3 = Lamp(3, 12)
lamps = [lamp1, lamp2, lamp3]

for lamp in lamps:
    lamp.load_in_data()
    """
    fig, ax = lamp.plot_all_data()
    plt.tight_layout()
    plt.show()
    """


D = D_He_sterk

golf_l1 = lamp1.bck_data[0]
golf_l1_err = lamp1.bck_data_err[0]

incoming_I_l1 = lamp1.bck_data[1]
incoming_I_l1_err = lamp1.bck_data_err[1]

outgoing_I_l1 = lamp1.helium_sterk_data[1]
outgoing_I_l1_err = lamp1.helium_sterk_data_err[1]

incoming_I_l2 = lamp2.bck_data[1]
incoming_I_l2_err = lamp2.bck_data_err[1]

outgoing_I_l2 = lamp2.helium_sterk_data[1]
outgoing_I_l2_err = lamp2.helium_sterk_data_err[1]

alpha_nu = []
alpha_nu_err = []
eta_nu = []
eta_nu_err = []

alpha_error_func = TRANSFER.analytical_alpha_error()
eta_error_func = TRANSFER.analytical_eta_error()

for i in range(0, len(golf_l1)):
    alpha, alpha_err = TRANSFER.analytical_alpha(incoming_I_l1[i], outgoing_I_l1[i],
                                                 incoming_I_l2[i], outgoing_I_l2[i],
                                                 D, 
                                                 incoming_I_l1_err[i], outgoing_I_l1_err[i],
                                                 incoming_I_l2_err[i], outgoing_I_l2_err[i],
                                                 0.5,
                                                 alpha_error_func)
    eta, eta_err = TRANSFER.analytical_eta(incoming_I_l1[i], outgoing_I_l1[i],
                                            incoming_I_l2[i], outgoing_I_l2[i],
                                            D, 
                                            incoming_I_l1_err[i], outgoing_I_l1_err[i],
                                            incoming_I_l2_err[i], outgoing_I_l2_err[i],
                                            0.5,
                                            eta_error_func)
    alpha_nu.append(alpha)
    alpha_nu_err.append(alpha_err)
    eta_nu.append(eta)
    eta_nu_err.append(eta_err)



golf = golf_l1
golf_err = golf_l1_err

fig, ax = plt.subplots(nrows=1, ncols=2)

ax[0].errorbar(golf, alpha_nu, yerr=alpha_nu_err, xerr=golf_err,
                        
                   label="Calculations", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)
ax[0].set_ylabel("$\\alpha_{\\nu}$")
ax[0].set_xlabel("Wavelength [nm]")
ax[0].set_title("Extinction coefficient")

ax[0].legend()

ax[1].errorbar(golf, eta_nu, yerr=eta_nu_err, xerr=golf_err,
                        
                   label="Calculations", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)
ax[1].set_ylabel("$\\eta_{\\nu}$")
ax[1].set_xlabel("Wavelength [nm]")
ax[1].set_title("Emission coefficient")

ax[1].legend()

plt.tight_layout()
plt.show()