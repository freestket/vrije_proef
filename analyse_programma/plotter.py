import numpy as np
import matplotlib.pyplot as plt
from lamp import Lamp
"""
This library contains functions to create figures on which alpha and eta will be plotted.
"""
    
lamp1 = Lamp(4, 6)
lamp2 = Lamp(5, 4)
lamp1.load_in_data()
lamp2.load_in_data()


def plot_all_relative_spectra(lamp: Lamp, helium: bool, pure: bool, fsize, titsize):
    """
    Plots the relative spectra of a lamp.

    Args:
        lamp (Lamp): Lamp to plot data for.
        helium (bool): Whether helium measurements will be plotted.
        pure (bool): Whether pure or commercial helium will be plotted.
        fsize (int): Fontsize for labels.
        titsize (int): Title size for plots.
    """
    lamp.make_relative_spectrums(True)
    lamp.make_relative_spectrums(False)

    lampnr = lamp.lamp_nr - 3

    fig1, ax1 = plt.subplots(dpi=200)

    if helium:

        if pure:
            helium_rel_data = lamp.helium_sterk_rel_data
            helium_rel_data_err = lamp.helium_sterk_rel_data_err

            ax1.errorbar(helium_rel_data[0], helium_rel_data[1], yerr=helium_rel_data_err[1],
                                    
                    label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

            ax1.set_ylabel("$I$ [counts]", fontsize=fsize)
            ax1.set_xlabel("Wavelength [nm]", fontsize=fsize)
            ax1.set_title(f"Outgoing radiation, pure helium", fontsize=titsize)
            ax1.legend()

        else:
            helium_rel_data = lamp.helium_zwak_rel_data
            helium_rel_data_err = lamp.helium_zwak_rel_data_err


            ax1.errorbar(helium_rel_data[0], helium_rel_data[1], yerr=helium_rel_data_err[1],
                                    
                    label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

            ax1.set_ylabel("$I$ [counts]", fontsize=fsize)
            ax1.set_xlabel("Wavelength [nm]", fontsize=fsize)
            ax1.set_title(f"Outgoing radiation, commercial helium", fontsize=titsize)
            ax1.legend()
    else:

        ax1.errorbar(lamp.rel_bck_data[0], lamp.rel_bck_data[1], yerr=lamp.rel_bck_data_err[1],
                                
                    label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

        ax1.set_ylabel("$I$ [counts]", fontsize=fsize)
        ax1.set_xlabel("Wavelength [nm]", fontsize=fsize)
        ax1.set_title(f"Incoming radiation", fontsize=titsize)
        ax1.legend()

    plt.tight_layout()
    plt.show()


fsize = 24
titsize = 28

plot_all_relative_spectra(lamp1, helium=False, pure=False, fsize=fsize, titsize=titsize)
plot_all_relative_spectra(lamp1, helium=True, pure=False, fsize=fsize, titsize=titsize)
plot_all_relative_spectra(lamp1, helium=True, pure=True, fsize=fsize, titsize=titsize)
plot_all_relative_spectra(lamp2, helium=False, pure=False, fsize=fsize, titsize=titsize)
plot_all_relative_spectra(lamp2, helium=True, pure=False, fsize=fsize, titsize=titsize)
plot_all_relative_spectra(lamp2, helium=True, pure=True, fsize=fsize, titsize=titsize)
