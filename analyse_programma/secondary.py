import data_reader as DATA
import transfert_vgl as TRANSFER
import matplotlib.pyplot as plt
from lamp import Lamp
import tools_experimentele.easystats as STAT


#Difference bckground - Helium

def plot_relative_spectrum(lamp_nr: int):

    lamp1 = Lamp(lamp_nr, 6)
    lamp1.load_in_data()

    lamp1_bck = lamp1.bck_data
    lamp1_bck_err = lamp1.bck_data_err

    lamp1_helium = lamp1.helium_zwak_data
    lamp1_helium_err = lamp1.helium_zwak_data_err


    golf = lamp1_bck[0]
    relative_intensity = []
    relative_intensity_err = []
    for i in range(0, len(lamp1_bck[1])):
        relative_intensity.append(lamp1_helium[1][i] - lamp1_bck[1][i])
        relative_intensity_err.append(STAT.foutpropagatie_som(1, -1, lamp1_helium_err[1][i], lamp1_bck_err[1][i]))


    fig, ax = plt.subplots()

    ax.errorbar(golf, relative_intensity, yerr=relative_intensity_err,
                            
                    label="Spectrum", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

    ax.set_ylabel("$I$ [counts]")
    ax.set_xlabel("Wavelength [nm]")
    ax.set_title("Spectrum")
    ax.legend()

    plt.tight_layout()
    plt.show()


plot_relative_spectrum(lamp_nr=4)