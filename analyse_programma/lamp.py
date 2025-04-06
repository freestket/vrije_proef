import data_reader as DATA
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("..")

class Lamp():
    """
    A class that contains all data related to a specific lamp.
    """

    def __init__(self, lamp_nr: int, voltage: int):
        """
        Lamp constructor.

        Args:
            lamp_nr (int): The number of the lamp: 1, 2 or 3.
            voltage (int): Voltage the lamp was connected to.

        Raises:
            ValueError: Lamp number is not 1, 2 or 3.
            ValueError: Voltage is negative.
        """
        if (lamp_nr < 1 or lamp_nr > 3) or (type(lamp_nr) != int):
            raise ValueError("lamp_nr has to be 1, 2 or 3")
        
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



    def load_in_data(self):
        """
        Loads in the data for the relevant lamp.

        Raises:
            ValueError: If the lamp does not have a valid number.
            ValueError: If a directory does not have the correct name.
            ValueError: If the wavelengths in the data files do not correspond
        """
        situation_directories = ["bck", "bck_noballon", "helium_zwak", "helium_sterk"]

        #Alle vier situaties inladen
        for dir_situation in situation_directories:

            #Relevante waarden voor for loop instellen
            i_modifier = 0
            if dir_situation == "bck":
                if self.lamp_nr == 1:
                    begin = 62
                    end = 93
                elif self.lamp_nr == 2:
                    begin = 155
                    end = 186
                elif self.lamp_nr == 3:
                    begin = 248
                    end = 279
                else:
                    raise ValueError("Not a valid lamp number")
                
            elif dir_situation == "bck_noballon":
                if self.lamp_nr == 1:
                    begin = 372
                    end = 403
                elif self.lamp_nr == 2:
                    begin = 434
                    end = 465
                    i_modifier = 31
                elif self.lamp_nr == 3:
                    begin = 341
                    end = 372
                else:
                    raise ValueError("Not a valid lamp number")

            elif dir_situation == "helium_zwak":
                if self.lamp_nr == 1:
                    begin = 93
                    end = 124
                elif self.lamp_nr == 2:
                    begin = 186
                    end = 217
                elif self.lamp_nr == 3:
                    begin = 279
                    end = 310
                else:
                    raise ValueError("Not a valid lamp number")
                
            elif dir_situation == "helium_sterk":
                if self.lamp_nr == 1:
                    begin = 124
                    end = 155
                elif self.lamp_nr == 2:
                    begin = 217
                    end = 248
                elif self.lamp_nr == 3:
                    begin = 310
                    end = 341
                else:
                    raise ValueError("Not a valid lamp number")
            else:
                raise ValueError("Not a valid directory name")


            #Gemiddelde van de 31 metingen bepalen
            avg_data = [[], []]
            avg_data_err = [None, []]
            for i, j in zip(range(0, 31), range(begin, end)):

                data = DATA.load_data_file(f"./data/lamp_{self.lamp_nr}_{dir_situation}/lamp{self.lamp_nr}{dir_situation}_Subt4__{i+i_modifier}__{j}.txt",
                                            header_row_number=15,
                                            delimiter="\t",
                                            converter_needed=False)
                for k in range(0, len(data)):
                    
                    if i == 0:
                        avg_data[0].append(data[k][0])
                        avg_data[1].append(data[k][1]) 
                    else:
                        if avg_data[0][k] != data[k][0]:
                            raise ValueError("Wavelengths do not correspond")
                        
                        avg_data[1][k] += data[k][1]

            for k in range(0, len(avg_data[1])):
                avg_data[1][k] = avg_data[1][k]/31



            for i, j in zip(range(0, 31), range(begin, end)):

                data = DATA.load_data_file(f"./data/lamp_{self.lamp_nr}_{dir_situation}/lamp{self.lamp_nr}{dir_situation}_Subt4__{i+i_modifier}__{j}.txt",
                                            header_row_number=15,
                                            delimiter="\t",
                                            converter_needed=False)
                
                for k in range(0, len(data)):
                    if i == 0:
                        avg_data_err[1].append((avg_data[1][k] - data[k][1])**2)
                    else:
                        avg_data_err[1][k] += (avg_data[1][k] - data[k][1])**2


            for k in range(0, len(avg_data_err[1])):
                avg_data_err[1][k] = 1.94*(avg_data_err[1][k]/(30))/(np.sqrt(31))

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
        if not (situation in ["bck", "bck_noballon", "helium_zwak", "helium_sterk"]):
            raise ValueError("Situation is not defined")
        

        match situation:
            case "bck":
                golf = self.bck_data[0]
                intensity = self.bck_data[1]

                golf_err = self.bck_data_err[0]
                intensity_err = self.bck_data_err[1]

                title = "Incoming intensity, lamp " + str(self.lamp_nr) + " (With balloon)"

            case "bck_noballon":
                golf = self.bck_noballon_data[0]
                intensity = self.bck_noballon_data[1]

                golf_err = self.bck_noballon_data_err[0]
                intensity_err = self.bck_noballon_data_err[1]

                title = "Incoming intensity, lamp " + str(self.lamp_nr) + " (Without balloon)"

            case "helium_zwak":
                golf = self.helium_zwak_data[0]
                intensity = self.helium_zwak_data[1]

                golf_err = self.helium_zwak_data_err[0]
                intensity_err = self.helium_zwak_data_err[1]

                title = "Outgoing intensity, lamp " + str(self.lamp_nr) + " (Commercial helium)"

            case "helium_sterk":
                golf = self.helium_sterk_data[0]
                intensity = self.helium_sterk_data[1]

                golf_err = self.helium_sterk_data_err[0]
                intensity_err = self.helium_sterk_data_err[1]

                title = "Outgoing intensity, lamp " + str(self.lamp_nr) + " (Pure helium)"


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