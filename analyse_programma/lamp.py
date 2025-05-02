import data_reader as DATA
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")
import tools_experimentele.easystats as STAT

class Lamp():
    """
    A class that contains all data related to a specific lamp.
    """

    def __init__(self, lamp_nr: int, voltage: int):
        """
        Lamp constructor.

        Args:
            lamp_nr (int): The number of the lamp.
            voltage (int): Voltage the lamp was connected to.

        Raises:
            ValueError: Voltage is negative.
        """

        if voltage < 0:
            raise ValueError("Voltage should be positive")

        self.lamp_nr = lamp_nr
        self.voltage = voltage
        self.name = "lamp " + str(lamp_nr)

        self.bck_data = []
        self.bck_data_err = []

        self.bck_noballon_data = []
        self.bck_noballon_data_err = []

        self.helium_zwak_data = []
        self.helium_zwak_data_err = []

        self.helium_sterk_data = []
        self.helium_sterk_data_err = []

        self.helium_zwak_dubbel_data = []
        self.helium_zwak_dubbel_data_err = []

        self.bck_dubbel_data = []
        self.bck_dubbel_data_err = []

        self.bck_noballon_dubbel_data = []
        self.bck_noballon_dubbel_data_err = []

        self.rel_bck_data = []
        self.rel_bck_data_err = []

        self.helium_sterk_rel_data = []
        self.helium_sterk_rel_data_err = []

        self.helium_zwak_rel_data = []
        self.helium_zwak_rel_data_err = []



    def load_in_data(self):
        """
        Loads in the data for the relevant lamp.

        Raises:
            ValueError: If the lamp does not have a valid number.
            ValueError: If a directory does not have the correct name.
            ValueError: If the wavelengths in the data files do not correspond
        """
        if self.lamp_nr == 4:
            situation_directories = ["bck", "bck_noballon", "helium_zwak", "helium_sterk", "bck_dubbel", "bck_noballon_dubbel", "helium_zwak_dubbel"]
        else:
            situation_directories = ["bck", "bck_noballon", "helium_zwak", "helium_sterk"]

        #Alle vier situaties inladen
        for dir_situation in situation_directories:

            #Relevante waarden voor for loop instellen
            i_modifier = 0
            subt = "Subt4"
            if dir_situation == "bck":
                if self.lamp_nr == 1:
                    begin = 62
                    end = 93
                    file_amount = 31
                elif self.lamp_nr == 2:
                    begin = 155
                    end = 186
                    file_amount = 31
                elif self.lamp_nr == 3:
                    begin = 248
                    end = 279
                    file_amount = 31
                elif self.lamp_nr == 4:
                    begin = 500
                    end = 600
                    file_amount = 100
                    subt = "Subt2"
                elif self.lamp_nr == 5:
                    begin = 255
                    end = 355
                    file_amount = 100
                else:
                    raise ValueError("Not a valid lamp number")
                
            elif dir_situation == "bck_noballon":
                if self.lamp_nr == 1:
                    begin = 372
                    end = 403
                    file_amount = 31
                elif self.lamp_nr == 2:
                    begin = 434
                    end = 465
                    i_modifier = 31
                    file_amount = 31
                elif self.lamp_nr == 3:
                    begin = 341
                    end = 372
                    file_amount = 31
                elif self.lamp_nr == 4:
                    begin = 200
                    end = 300
                    file_amount = 100
                    subt = "Subt2"
                elif self.lamp_nr == 5:
                    begin = 355
                    end = 455
                    file_amount = 100
                else:
                    raise ValueError("Not a valid lamp number")

            elif dir_situation == "helium_zwak":
                if self.lamp_nr == 1:
                    begin = 93
                    end = 124
                    file_amount = 31
                elif self.lamp_nr == 2:
                    begin = 186
                    end = 217
                    file_amount = 31
                elif self.lamp_nr == 3:
                    begin = 279
                    end = 310
                    file_amount = 31
                elif self.lamp_nr == 4:
                    begin = 400
                    end = 500
                    file_amount = 100
                    subt = "Subt2"
                elif self.lamp_nr == 5:
                    begin = 155
                    end = 255
                    file_amount = 100
                else:
                    raise ValueError("Not a valid lamp number")
                
            elif dir_situation == "helium_sterk":
                if self.lamp_nr == 1:
                    begin = 124
                    end = 155
                    file_amount = 31
                elif self.lamp_nr == 2:
                    begin = 217
                    end = 248
                    file_amount = 31
                elif self.lamp_nr == 3:
                    begin = 310
                    end = 341
                    file_amount = 31
                elif self.lamp_nr == 4:
                    begin = 100
                    end = 200
                    file_amount = 100
                    subt = "Subt2"
                elif self.lamp_nr == 5:
                    begin = 0
                    end = 100
                    file_amount = 100
                    subt = "Subt2"
                else:
                    raise ValueError("Not a valid lamp number")
            elif dir_situation == "bck_noballon_dubbel":
                if self.lamp_nr == 4:
                    file_amount = 100
                    begin = 900
                    end = 1000
                    subt = "Subt2"
                    i_modifier = 100
                else:
                    raise ValueError("Not a valid lamp number")

            elif dir_situation == "bck_dubbel":
                if self.lamp_nr == 4:
                    file_amount = 100
                    begin = 1000
                    end = 1100
                    subt = "Subt2"
                else:
                    raise ValueError("Not a valid lamp number")

            elif dir_situation == "helium_zwak_dubbel":
                if self.lamp_nr == 4:
                    file_amount = 100
                    begin = 700
                    end = 800
                    subt = "Subt2"
                    i_modifier = 100
            
            else:
                raise ValueError("Not a valid directory name")


            #Gemiddelde van de 31 metingen bepalen
            avg_data = [[], []]
            avg_data_err = [None, []]
            for i, j in zip(range(0, file_amount), range(begin, begin + file_amount)):

                golf, intens = DATA.load_data_file(f"./data/lamp_{self.lamp_nr}_{dir_situation}/lamp{self.lamp_nr}{dir_situation}_{subt}__{i+i_modifier}__{j}.txt",
                                            header_row_number=15,
                                            delimiter="\t",
                                            converter_needed=False)
                for k in range(0, len(intens)):
                    
                    if i == 0:
                        avg_data[0].append(golf[k])
                        avg_data[1].append(intens[k]) 
                    else:
                        if avg_data[0][k] != golf[k]:
                            raise ValueError("Wavelengths do not correspond")
                        
                        avg_data[1][k] += intens[k]

            for k in range(0, len(avg_data[1])):
                avg_data[1][k] = avg_data[1][k]/file_amount



            for i, j in zip(range(0, file_amount), range(begin, begin + file_amount)):

                golf, intens = DATA.load_data_file(f"./data/lamp_{self.lamp_nr}_{dir_situation}/lamp{self.lamp_nr}{dir_situation}_{subt}__{i+i_modifier}__{j}.txt",
                                            header_row_number=15,
                                            delimiter="\t",
                                            converter_needed=False)
                
                for k in range(0, len(intens)):
                    if i == 0:
                        avg_data_err[1].append((avg_data[1][k] - intens[k])**2)
                    else:
                        avg_data_err[1][k] += (avg_data[1][k] - intens[k])**2


            for k in range(0, len(avg_data_err[1])):
                avg_data_err[1][k] = 1.94*(avg_data_err[1][k]/(file_amount-1))/(np.sqrt(file_amount))

            avg_data_err[0] = [0.005 for i in avg_data[0]]



            match dir_situation:
                case "bck":
                    self.bck_data = avg_data
                    self.bck_data_err = avg_data_err
                case "bck_noballon":
                    self.bck_noballon_data = avg_data
                    self.bck_noballon_data_err = avg_data_err
                case "helium_sterk":
                    self.helium_sterk_data = avg_data
                    self.helium_sterk_data_err = avg_data_err
                case "helium_zwak":
                    self.helium_zwak_data = avg_data
                    self.helium_zwak_data_err = avg_data_err
                case "bck_dubbel":
                    self.bck_dubbel_data = avg_data
                    self.bck_dubbel_data_err = avg_data_err
                case "bck_noballon_dubbel":
                    self.bck_noballon_dubbel_data = avg_data
                    self.bck_noballon_dubbel_data_err = avg_data_err
                case "helium_zwak_dubbel":
                    self.helium_zwak_dubbel_data = avg_data
                    self.helium_zwak_dubbel_data_err = avg_data_err



    def plot_dataset(self, situation: str, fig = None, ax = None, pos1: int = None, pos2: int = None):
        """
        Plots the data of a specific situation on a new figure or a provided figure and position and returns this.

        Args:
            situation (str): The situation to be plotted.
            fig (plt.fig, optional): The figure to plot on. Defaults to None.
            ax (plt.ax, optional): The corresponding ax object to plot on. Defaults to None.
            pos1 (int, optional): First index to plot on the ax object. Defaults to None.
            pos2 (int, optional): Second index to plot on the ax object. Defaults to None.

        Raises:
            ValueError: If the situation is not a valid option.
            ValueError: If any needed parameter is missing.

        Returns:
            plt.fig, plt.ax: The figure and ax objects with the new graph plotted on it.
        """
        if not (situation in ["bck", "bck_noballon", "helium_zwak", "helium_sterk", "bck_dubbel", "bck_noballon_dubbel", "helium_zwak_dubbel"]):
            raise ValueError("Situation is not defined")
        
        if self.lamp_nr == 4:
            lamp_nr = 1
        elif self.lamp_nr == 5:
            lamp_nr = 2
        else:
            lamp_nr = self.lamp_nr

        match situation:
            case "bck":
                golf = self.bck_data[0]
                intensity = self.bck_data[1]

                golf_err = self.bck_data_err[0]
                intensity_err = self.bck_data_err[1]

                title = "Incoming intensity, lamp " + str(lamp_nr) + " (With balloon)"

            case "bck_noballon":
                golf = self.bck_noballon_data[0]
                intensity = self.bck_noballon_data[1]

                golf_err = self.bck_noballon_data_err[0]
                intensity_err = self.bck_noballon_data_err[1]

                title = "Incoming intensity, lamp " + str(lamp_nr) + " (Without balloon)"

            case "helium_zwak":
                golf = self.helium_zwak_data[0]
                intensity = self.helium_zwak_data[1]

                golf_err = self.helium_zwak_data_err[0]
                intensity_err = self.helium_zwak_data_err[1]

                title = "Outgoing intensity, lamp " + str(lamp_nr) + " (Commercial helium)"

            case "helium_sterk":
                golf = self.helium_sterk_data[0]
                intensity = self.helium_sterk_data[1]

                golf_err = self.helium_sterk_data_err[0]
                intensity_err = self.helium_sterk_data_err[1]

                title = "Outgoing intensity, lamp " + str(lamp_nr) + " (Pure helium)"

            case "bck_dubbel":
                golf = self.bck_dubbel_data[0]
                intensity = self.bck_dubbel_data[1]

                golf_err = self.bck_dubbel_data_err[0]
                intensity_err = self.bck_dubbel_data_err[1]

                title = "Incoming intensity, lamp " + str(lamp_nr) + " (With balloons, double balloons)"

            case "bck_noballon_dubbel":
                golf = self.bck_noballon_dubbel_data[0]
                intensity = self.bck_noballon_dubbel_data[1]

                golf_err = self.bck_noballon_dubbel_data_err[0]
                intensity_err = self.bck_noballon_dubbel_data_err[1]

                title = "Incoming intensity, lamp " + str(lamp_nr) + " (Without balloon, double balloon distance)"

            case "helium_zwak_dubbel":
                golf = self.helium_zwak_dubbel_data[0]
                intensity = self.helium_zwak_dubbel_data[1]

                golf_err = self.helium_zwak_dubbel_data_err[0]
                intensity_err = self.helium_zwak_dubbel_data_err[1]

                title = "Outgoing intensity, lamp " + str(lamp_nr) + " (Commercial helium, double balloons)"


        if fig == None and ax == None and pos1 == None and pos2 == None:
            fig, ax = plt.subplots(nrows=1, ncols=1)

            ax.errorbar(golf, intensity, yerr=intensity_err, xerr=golf_err,
                        
                        label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)
            
            ax.set_ylabel("$I$ [counts]")
            ax.set_xlabel("Wavelength [nm]")
            ax.set_title(title)
            ax.legend()

        elif fig == None or ax.any() == None or pos1 == None or pos2 == None:
            raise ValueError("Plotting functions is missing a needed parameter")
        
        else:
            ax[pos1][pos2].errorbar(golf, intensity, yerr=intensity_err, xerr=golf_err,
                                    
                                    label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)
            
            ax[pos1][pos2].set_ylabel("$I$ [counts]")
            ax[pos1][pos2].set_xlabel("Wavelength [nm]")
            ax[pos1][pos2].set_title(title)
            ax[pos1][pos2].legend()

        return fig, ax
    

    def plot_all_data(self):
        """
        Plots the data of all situations of this lamp onto a figure.

        Returns:
            plt.fig, plt.ax: The figure and ax objects with all situations plotted.
        """
        situations = ["bck", "bck_noballon", "helium_zwak", "helium_sterk"]

        fig, ax = plt.subplots(nrows=2, ncols=2)

        for i in range(0, 2):
            for j in range(0, 2):
                if i == 0:
                    fig, ax = self.plot_dataset(situations[i+j], fig, ax, i, j)
                elif i == 1:
                    fig, ax = self.plot_dataset(situations[i+j+1],fig, ax, i, j)

        return fig, ax
    
    def plot_dubbel_data(self):
        """
        Plots the data of all situations where a double ballon was used and situations with a single balloon as reference.

        Returns:
            plt.fig, plt.ax: The figure and ax objects with described situations plotted.
        """
        situations = ["bck", "bck_noballon", "helium_zwak", "bck_dubbel", "bck_noballon_dubbel", "helium_zwak_dubbel"]

        fig, ax = plt.subplots(nrows=3, ncols=2)

        for i in range(0, 3):
            for j in range(0, 2):
                if i == 0:
                    fig, ax = self.plot_dataset(situations[i+j], fig, ax, i, j)
                elif i == 1:
                    fig, ax = self.plot_dataset(situations[i+j+1], fig, ax, i, j)
                elif i == 2:
                    fig, ax = self.plot_dataset(situations[i+j+2], fig, ax, i, j)
        
        return fig, ax



    def make_relative_spectrums(self, pure_helium: bool):

        rel_bck = self.bck_noballon_data
        rel_bck_err = self.bck_noballon_data_err

        lamp1_bck = self.bck_data
        lamp1_bck_err = self.bck_data_err

        if pure_helium:
            lamp1_helium = self.helium_sterk_data
            lamp1_helium_err = self.helium_sterk_data_err

        else:
            lamp1_helium = self.helium_zwak_data
            lamp1_helium_err = self.helium_zwak_data_err


        golf = lamp1_bck[0]
        golf_err = lamp1_bck_err[0]

        relative_intensity_bck = []
        relative_intensity_bck_err = []
        for i in range(0, len(rel_bck[1])):
            relative_intensity_bck.append(-lamp1_bck[1][i] + rel_bck[1][i])
            relative_intensity_bck_err.append(STAT.foutpropagatie_som(-1, 1, lamp1_bck_err[1][i], rel_bck_err[1][i]))

        relative_intensity = []
        relative_intensity_err = []
        for i in range(0, len(rel_bck[1])):
            if False: #self.lamp_nr == 4 and pure_helium:
                relative_intensity.append(lamp1_helium[1][i] - rel_bck[1][i])
                relative_intensity_err.append(STAT.foutpropagatie_som(1, -1, lamp1_helium_err[1][i], rel_bck_err[1][i]))
            else:
                relative_intensity.append(-lamp1_helium[1][i] + rel_bck[1][i])
                relative_intensity_err.append(STAT.foutpropagatie_som(-1, 1, lamp1_helium_err[1][i], rel_bck_err[1][i]))


        

        self.rel_bck_data.append(golf) 
        self.rel_bck_data.append(relative_intensity_bck)
 
        self.rel_bck_data_err.append(golf_err)
        self.rel_bck_data_err.append(relative_intensity_bck_err)

        if pure_helium:
            self.helium_sterk_rel_data.append(golf)
            self.helium_sterk_rel_data.append(relative_intensity)

            self.helium_sterk_rel_data_err.append(golf)
            self.helium_sterk_rel_data_err.append(relative_intensity_err)

        else:
            self.helium_zwak_rel_data.append(golf)
            self.helium_zwak_rel_data.append(relative_intensity)

            self.helium_zwak_rel_data_err.append(golf)
            self.helium_zwak_rel_data_err.append(relative_intensity_err)


    def plot_relative_spectra(self, pure_helium: bool = True):
        
        self.make_relative_spectrums(pure_helium)

        fig1, ax1 = plt.subplots(ncols=2, nrows=1)

        if pure_helium:
            helium_rel_data = self.helium_sterk_rel_data
            helium_rel_data_err = self.helium_sterk_rel_data_err

            hel = "pure"

        else:
            helium_rel_data = self.helium_zwak_rel_data
            helium_rel_data_err = self.helium_zwak_rel_data_err

            hel = "commercial"

        ax1[0].errorbar(self.rel_bck_data[0], self.rel_bck_data[1], yerr=self.rel_bck_data_err[1],
                                
                        label="Spectrum", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

        ax1[0].set_ylabel("$I$ [counts]")
        ax1[0].set_xlabel("Wavelength [nm]")
        ax1[0].set_title("Spectrum: Incoming radiation")
        ax1[0].legend()

        ax1[1].errorbar(helium_rel_data[0], helium_rel_data[1], yerr=helium_rel_data_err[1],
                                
                        label="Spectrum", fmt=" ", marker="o", color="black", ecolor="black", markersize=1, capsize=1.5, capthick=0.5, elinewidth=0.5)

        ax1[1].set_ylabel("$I$ [counts]")
        ax1[1].set_xlabel("Wavelength [nm]")
        ax1[1].set_title("Spectrum: outgoing radiation")
        ax1[1].legend()

        fig1.suptitle(f"Lamp {self.lamp_nr}, using {hel} helium. ", fontsize=16)

        return fig1, ax1
    
    
    def plot_all_relative_spectra(self):

        self.make_relative_spectrums(True)
        self.make_relative_spectrums(False)

        fig1, ax1 = plt.subplots(ncols=1, nrows=3, dpi=190)

        helium_rel_data = self.helium_sterk_rel_data
        helium_rel_data_err = self.helium_sterk_rel_data_err


        ax1[0].errorbar(self.rel_bck_data[0], self.rel_bck_data[1], yerr=self.rel_bck_data_err[1],
                                
                        label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=0.8, capsize=1, capthick=0.3, elinewidth=0.3)

        ax1[0].set_ylabel("$I$ [counts]")
        ax1[0].set_xlabel("Wavelength [nm]")
        ax1[0].set_title("Incoming radiation")
        ax1[0].legend()


        ax1[1].errorbar(helium_rel_data[0], helium_rel_data[1], yerr=helium_rel_data_err[1],
                                
                        label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=0.8, capsize=1, capthick=0.3, elinewidth=0.3)

        ax1[1].set_ylabel("$I$ [counts]")
        ax1[1].set_xlabel("Wavelength [nm]")
        ax1[1].set_title("Outgoing radiation through pure helium")
        ax1[1].legend()


        helium_rel_data = self.helium_zwak_rel_data
        helium_rel_data_err = self.helium_zwak_rel_data_err


        ax1[2].errorbar(helium_rel_data[0], helium_rel_data[1], yerr=helium_rel_data_err[1],
                                
                        label="Data", fmt=" ", marker="o", color="black", ecolor="black", markersize=0.8, capsize=1, capthick=0.3, elinewidth=0.3)

        ax1[2].set_ylabel("$I$ [counts]")
        ax1[2].set_xlabel("Wavelength [nm]")
        ax1[2].set_title("Outgoing radiation through commercial helium")
        ax1[2].legend()

        if self.lamp_nr == 4 or self.lamp_nr == 5:
            lampnr = self.lamp_nr - 3

        fig1.suptitle(f"Lamp {lampnr}", fontsize=14)

        return fig1, ax1