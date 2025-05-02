import data_reader as DATA
import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
import tools_experimentele.easystats as STAT


#Difference bckground - Helium

def plot_relative_spectrum(lamp_nr: int):

    lamp1 = Lamp(lamp_nr, 6)
    lamp1.load_in_data()

    rel_bck = lamp1.bck_data
    rel_bck_err = lamp1.bck_data_err

    lamp1_bck = lamp1.bck_noballon_data
    lamp1_bck_err = lamp1.bck_noballon_data_err

    lamp1_helium = lamp1.helium_sterk_data
    lamp1_helium_err = lamp1.helium_sterk_data_err


    golf = lamp1_bck[0]

    relative_intensity_bck = []
    relative_intensity_bck_err = []
    for i in range(0, len(rel_bck[1])):
        relative_intensity_bck.append(lamp1_bck[1][i] - rel_bck[1][i])
        relative_intensity_bck_err.append(STAT.foutpropagatie_som(1, -1, lamp1_bck_err[1][i], rel_bck_err[1][i]))

    relative_intensity = []
    relative_intensity_err = []
    for i in range(0, len(rel_bck[1])):
        relative_intensity.append(lamp1_helium[1][i] - rel_bck[1][i])
        relative_intensity_err.append(STAT.foutpropagatie_som(1, -1, lamp1_helium_err[1][i], rel_bck_err[1][i]))


    fig1, ax1 = plt.subplots(ncols=2, nrows=1)

    ax1[0].errorbar(golf, relative_intensity_bck, yerr=relative_intensity_bck_err,
                            
                    label="Spectrum", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

    ax1[0].set_ylabel("$I$ [counts]")
    ax1[0].set_xlabel("Wavelength [nm]")
    ax1[0].set_title("Spectrum: Incoming radiation")
    ax1[0].legend()

    ax1[1].errorbar(golf, relative_intensity, yerr=relative_intensity_err,
                            
                    label="Spectrum", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

    ax1[1].set_ylabel("$I$ [counts]")
    ax1[1].set_xlabel("Wavelength [nm]")
    ax1[1].set_title("Spectrum: outgoing radiation")
    ax1[1].legend()

    fig1.suptitle(f"Lamp {lamp_nr}", fontsize=16)

    #plt.tight_layout()
    #plt.show()

    return relative_intensity_bck, relative_intensity_bck_err, relative_intensity, relative_intensity_err



def getRelativeLamp(lamp_nr: int):

    rel_bck, rel_bck_err, rel_int, rel_int_err = plot_relative_spectrum(lamp_nr=lamp_nr)

    testLamp = Lamp(lamp_nr, 6)
    testLamp.load_in_data()
    testLamp.bck_data[1] = rel_bck
    testLamp.bck_data_err[1] = rel_bck_err
    testLamp.helium_sterk_data[1] = rel_int
    testLamp.helium_sterk_data_err[1] = rel_int_err

    return testLamp



newLamp4 = getRelativeLamp(2)
newLamp5 = getRelativeLamp(4)



D_He_zwak_2 = 23.4e-2
D_He_sterk_2 = 25.3e-2
D_lucht_2 = 24.7e-2

d_err = 0.3e-2



fig, ax, alpha_nu, alpha_nu_err, eta_nu, eta_nu_err, golf = TRANSFER.calculate_alpha_eta(newLamp4, newLamp5, D_He_sterk_2, d_err, pure_helium=True, no_ballon_bck=False)

plt.tight_layout()
plt.show()



#Plot de source function (eta_nu / alpha_nu)
BB = []
BB_err = []
for i in range(0, len(alpha_nu)):
    BB.append(eta_nu[i]/alpha_nu[i])
    BB_err.append(STAT.foutpropagatie_product(1, -1, eta_nu_err[i], alpha_nu_err[i], eta_nu[i], alpha_nu[i], BB[i]))

fig, ax = plt.subplots()

ax.errorbar(golf, BB, yerr=BB_err,
                        
                label="Calculations", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

plt.tight_layout()
plt.legend()
plt.show()