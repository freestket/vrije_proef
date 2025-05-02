

# Vrije proef - Experimentele Basistechnieken

Charlotte Vincent, Free Staquet

# TODO

## Software

- Extra documentation

## Experiment



# Determining extinction and emission coefficients of helium in front of a light source

## Idea

In the radiation transfer equation
$$\frac{dI_\nu}{ds} = \eta_\nu - \alpha_\nu I_\nu$$
two wavelength-dependent coefficients occur.
For example, in order to be able to analyze a nebula, these coefficients must be known for certain gases/substances. That is why we determine these for a frequently occurring gas in astronomy: helium.

### Developing the experiment

#### Setup

For the setup we prefer to use a darkened room, but the software (OceanView) also allows us to set a background spectrum.
A balloon filled with helium is hung up. The balloon is filled enough so that the walls thin out.
Behind the balloon a lamp is placed that is focused enough to illuminate only the balloon. This lamp is connected to a 12 V power source.
On the other side of the balloon, opposite the lamp, a digital spectrometer is placed and connected to a computer.
Along the edges of the balloon it is shielded as much as possible with black cloths to further limit the background radiation.

#### Measurements

The lamp is first connected to a 4 V voltage source.

##### Backgroundspectrum

We first set the background spectrum by replacing the helium balloon with a balloon of the same volume filled with air and then switching off the lamp. In this way, the influence of the air and the walls of the balloon are taken into account.
This is set as "Dark background spectrum" via the OceanView software.

##### Incoming Radiation

To measure the incident radiation ($I_\nu^{in}$) the lamp is turned back on and the air-filled balloon remains suspended.
The OceanView program then creates a data file containing the incident radiation over the wavelength spectrum.

##### Emerging Radiation

To measure the outgoing radiation ($I_\nu^{em}$), the air-filled balloon is replaced by the helium-filled balloon. The OceanView program then measures this radiation again over the wavelength spectrum and stores it in a data file.

##### Second set of Measurements -- Second Lamp

To make the analysis possible, the above procedure must be repeated with a lamp that emits a different spectrum. This can be done by connecting the same lamp to a lower voltage, for example 6 V.

#### Analyse

The obtained data is analyzed at each wavelength.
At each wavelength the following system of equations is solved:
$$I_1^{out} = I_1^{in} e^{-\alpha D} + \frac{\eta}{\alpha}(1 - e^{-\alpha D}) \\
I_2^{out} = I_2^{in} e^{-\alpha D} + \frac{\eta}{\alpha}(1 - e^{-\alpha D})$$
The coefficients $\alpha$ and $\eta$ can then be calculated using:
$$\alpha = \frac{\log{(\frac{I_1^{in} - I_2^{in}}{I_1^{out} - I_2^{out}})}}{D} \\
\eta = \frac{(I_1^{in}I_2^{out} - I_1^{out}I_2^{in})\log{(\frac{I_1^{in} - I_2^{in}}{I_1^{out} - I_2^{out}})}}{D(I_1^{in} - I_1^{out} - I_2^{in} + I_2^{out})}$$
This calculation is then repeated at each wavelength.
With these values, graphs are plotted for $\alpha_\nu$ and $\eta_\nu$ for helium.
This graph can then be discussed.

# Software

To keep an overview of the analysis, the software was divided into several files.

## main.py

This main file will run all the necessary analysis and eventually return a graph of the coefficients.
It is also used to note down other measurements that are not included in data files.

## data_reader.py

This file facilitates the reading of the data files.

### load_data_file(file_path: str, header_row_number: int = 0, delimiter: str = ",", converter_needed: bool = False) -> list:

Loads the data from the OceanView spectrometer data files.

Arguments:
    file_path (str): 
        The directory path to the file including the filename.
    header_row_number (int, optional): 
        The amount of rows the header takes up. Defaults to 0.
    delimiter (str, optional): 
        The character seperating the values in the data file. Defaults to ",".
    converter_needed (bool, optional): 
        Whether or not the data files need commas to be replaced with decimal points. Defaults to False.

Returns:
    list: 
        The raw data contained in a matrix.

### reformat_data(data_matrix_lamp1: list, data_matrix_lamp2: list) -> list:

Reformats the data to an easier to use format.

Args:
    data_matrix_lamp1 (list): The raw data read in by the load_data_file function for lamp 1.
    data_matrix_lamp2 (list): The raw data read in by the load_data_file function for lamp 2.

Raises:
    ValueError: When wavelengths of given data matrices do not correspond.

Returns:
    list: The reformatted data. Structured as [wavelength, lamp_1, lamp_2] for each element.

### seperate_data_lists(data: list) -> tuple: (Unused?)

Splits the data of "reformat_data" into 3 lists: wavlengths, lamp 1 intensity, lamp 2 intensity.

Args:
    data (list): The data matrix obtained by reformatting.

Raises:
    ValueError: When the data has not properly been reformatted.

Returns:
    tuple: A tuple consisting of three lists: wavelength, lamp 1 intensity, lamp 2 intensity

## transfert_vgl.py

This file calculates values for $\alpha$ and $\eta$.

### general_transfer_solution(I_in, alpha, eta, d):

Gives the outgoing intensity from the general solution of the radiation transfer equation.

Args:
    I_in (_type_): Ingoing intensity.
    alpha (_type_): Extinction coefficient.
    eta (_type_): Emission coefficient.
    d (_type_): Distance traveled by radiation.

Returns:
    _type_: Outgoing intensity.

### analytical_alpha_error():

Computes the function used to calculate the error on alpha.

Returns:
    callable: Error function for alpha.

### alytical_alpha(I_1_in: float, I_1_out: float, I_2_in: float, I_2_out: float, d: float) -> float:

Calculates the extinction coefficient at a given wavelength.

Args:
    I_1_in (float): Ingoing intensity of the first measurement.
    I_1_out (float): Outgoing intensity of the first measurement.
    I_2_in (float): Ingoing intensity of the second measurement.
    I_2_out (float): Outgoing intensity of the second measurement.
    d (float): Distance traveled by radiation.
    I_1_in_err (float): 
    I_1_out_err (float):
    I_2_in_err (float):
    I_2_out_err (float):
    d_err (float):

Returns:
    float: The emission coefficient on a given wavelength.
    float: Error on the emission coefficient.

### analytical_eta_error():

Computes the function that calculates the error on eta.

Returns:
    callable: Error function for eta.

### analytical_eta(I_1_in: float, I_1_out: float, I_2_in: float, I_2_out: float, d: float) -> float:

Calculates the lambdified error function for eta.

Returns:
    callable: Error function for eta.

### calculate_alpha_eta(lamp1 : Lamp, lamp2: Lamp, D: float, d_err: float, pure_helium: bool = False, no_ballon_bck: bool = False):

Calculates the graphs for alpha and eta and returns them in fig, ax objects.

Args:
    lamp1 (Lamp): First lamp.
    lamp2 (Lamp): Second lamp.
    D (float): Distance/diameter of the balloon.
    d_err (float): Error on the distance of the balloon.
    pure_helium (bool, optional): Whether or not pure helium data should be used. Defaults to False.
    no_ballon_bck (bool, optional): Whether or not no balloon was used in the incoming radiation. Defaults to False.

Returns:
    fig, ax: The figure with alpha and eta plotted onto it.

## plotter.py

This file makes figures used in the paper.

### plot_all_relative_spectra(lamp: Lamp, helium: bool, pure: bool, fsize, titsize):

Plots the relative spectra of a lamp.

Args:
    lamp (Lamp): Lamp to plot data for.
    helium (bool): Whether helium measurements will be plotted.
    pure (bool): Whether pure or commercial helium will be plotted.
    fsize (int): Fontsize for labels.
    titsize (int): Title size for plots.

## lamp.py

### Class Lamp()

This contains all the data for a particular lamp. Functions can be run separately per lamp using these classes.

#### \__init__(self, lamp_nr: int, voltage: int):

Constructor.

Args:
    lamp_nr (int): The number of the lamp.
    voltage (int): Voltage the lamp was connected to.

Raises:
    ValueError: Voltage is negative.

#### load_in_data(self):

Load all data for the different situations for this lamp.

For this function to work it is important that the names of folders and files in ./data/ do not change.

Raises:
    ValueError: If the lamp does not have a valid number.
    ValueError: If a directory does not have the correct name.
    ValueError: If the wavelengths in the data files do not correspond

#### plot_dataset(self, situation: str, fig = None, ax = None, pos1 = None, pos2 = None):

Plot the data for a given situation of this lamp.

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

#### plot_all_data(self):

Plot the data from all situations on one figure.

Returns:
    plt.fig, plt.ax: The figure and ax objects with all situations plotted.

#### plot_dubbel_data(self):

Plots the data of all situations where a double ballon was used and situations with a single balloon as reference.

Returns:
    plt.fig, plt.ax: The figure and ax objects with described situations plotted.

#### make_relative_spectrums(self, pure_helium: bool):

Makes the data lists for the lamp spectra, taking into account the air-filed balloon and lamp.

Args:
    pure_helium (bool): Whether or not pure or commercial helium is used.

#### plot_relative_spectra(self, pure_helium: bool = True):

Plots all the relative spectra for a lamp.

Args:
    pure_helium (bool, optional): Whether or not pure helium should be used. Defaults to True.

Returns:
    plt.fig, plt.ax: Fig and ax objects with spectra plotted onto them.

#### plot_all_relative_spectra(self):

Plots all the relative spectra of a lamp.

Returns:
    plt.fig, plt.ax: Fig and ax objects with all relative spectral data plotted onto them.

### test.py

Used during software development to test functionality without having to wait too long for the entire program to run.
The implemented functions are thus not documented.

# Voorbereiding

The file preparation.ipynb was used to determine an analytic solution for $\alpha$ and $\eta$ using the system introduced at the beginning of the Analysis section.
