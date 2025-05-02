import data_reader as DATA
import transfert_vgl as TRANSFER
import plotter as PLOT

import numpy as np
from lamp import Lamp
import matplotlib.pyplot as plt

import sys
sys.path.append("..")
"""
This file is used for testing the analysis program.

TODO:
    reformat_data_Test
    seperate_data_lists_Test
"""


def load_data_file_Test():      
    spectro_data = DATA.load_data_file("../spectroscopie/digitale_spectrometer_metingen/blauw_Absorbance__0__0.txt",
                                    header_row_number=15,
                                    delimiter='\t',
                                    converter_needed=True)


def reformat_data_Test():
    pass


def seperate_data_lists_Test():
    pass


def lamp_file_load_Test():
    lamp1 = Lamp(1, 10)
    lamp1.load_in_data()
    assert(len(lamp1.bck_data) == 2)
    assert(len(lamp1.bck_data_err) == 2)


def lamp_plot_all_data_Test(lampnr: int):
    lamp = Lamp(lampnr, 10)
    lamp.load_in_data()
    fig, ax = lamp.plot_all_data()
    plt.show()

def lamp4_dubbel_data():
    lamp4  = Lamp(4, 6)
    lamp4.load_in_data()
    fig, ax = lamp4.plot_dubbel_data()
    plt.show()

def lamp_rel_spectrum_plot(lampnr: int):
    lamp = Lamp(lampnr, 6)
    lamp.load_in_data()
    fig, ax = lamp.plot_all_relative_spectra()
    plt.show()





load_data_file_Test()
lamp_file_load_Test()
#lamp_plot_all_data_Test(lampnr=4)
#lamp4_dubbel_data()
lamp_rel_spectrum_plot(lampnr=4)
