

# Vrije proef - Experimentele Basistechnieken

Charlotte Vincent, Free Staquet

# TODO

## Software

- transfert_vgl.py 
- main.py
- plotter.py
- translations
- documentation

## Experiment

- Problemen met data lamp 1 en 3 bij puur helium uitzoeken

# Bepalen van extinctie- en emissiecoëfficiënten van helium voor een lichtbron

## Idee

In de transfertvergelijking
$$\frac{dI_\nu}{ds} = \eta_\nu - \alpha_\nu I_\nu$$
komen twee golflengte-afhankelijke coëfficiënten voor.
Om bijvoorbeeld een nevel te kunnen analyseren moeten deze coëfficiënten gekend zijn voor bepaalde gassen/stoffen. Daarom bepalen we deze dus voor een frequent voorkomend gas in de sterrenkunde: helium.

### Uitwerking

#### Opstelling

Voor de opstelling gebruiken we liefst een verduisterde ruimte, maar de software (OceanView) laat ook toe om een achtergrondspectrum in te stellen.
Er wordt een ballon opgehangen die gevuld is met helium. De ballon wordt genoeg gevuld zodat de wanden verdunnen.
Achter de ballon wordt een lamp geplaats die genoeg gefocuseerd is om alleen de ballon te beschijnen. Deze lamp wordt verbonden met een spanningsbron van 12 V.
Aan de andere kant van de ballon, tegenover de lamp wordt een digitale spectrometer geplaatst en verbonden met een computer.
Langs de randen van de ballon wordt deze met zwarte doeken zo goed als mogelijk afgeschermd om de achtergrondstraling verder te beperken.

#### Metingen

De lamp wordt eerst aangesloten op een spanningsbron van 12 V.

##### Achtergrondspectrum

We stellen eerst het achtergrondspectrum in door de heliumballong te vervangen door een ballon met hetzelfde volume die gevuld is met lucht en vervolgens de lamp uit te schakelen. Op deze manier wordt de invloed van de lucht en van de wanden van de ballon mee in rekening gehouden.
Via de OceanView software wordt dit ingesteld als "Dark backgroundspectrum".

##### Invallend straling

Om de invallende straling ($I_\nu^{in}$) te meten wordt de lamp terug aangezet en blijft de met lucht gevulde ballong hangen.
Er wordt dan met het OceanView programma een databestand gemaakt waarin de invallende straling over het golflengtespectrum staat.

##### Uitgaande straling

Voor de uitgaande straling ($I_\nu^{em}$) te meten wordt de met lucht gevulde ballon terug vervangen door de met helium gevulde ballon.
Het OceanView programma meet deze straling dan terug over het golflengtespectrum en slaagt dit op in een databestand.

##### Tweede set metingen -- Andere lamp

Voor de analyse mogelijk te maken moet de bovenstaande procedure nog eens herhaald worden met een lamp die een ander spectrum uitstraalt. Dit kan gedaan worden door dezelfde lamp op een lagere spanning aan te sluiten , bijvoorbeeld 6 V.

#### Analyse

De bekomen data wordt telkens geanalyseerd per golflengte.
Op elke golflengte wordt het volgende stelsel opgelost:
$$I_1^{out} = I_1^{in} e^{-\alpha D} + \frac{\eta}{\alpha}(1 - e^{-\alpha D}) \\
I_2^{out} = I_2^{in} e^{-\alpha D} + \frac{\eta}{\alpha}(1 - e^{-\alpha D})$$
De coëfficienten $\alpha$ en $\eta$ kunnen dan berekend worden met de volgende uitdrukkingen:
$$\alpha = \frac{\log{(\frac{I_1^{in} - I_2^{in}}{I_1^{out} - I_2^{out}})}}{D} \\
\eta = \frac{(I_1^{in}I_2^{out} - I_1^{out}I_2^{in})\log{(\frac{I_1^{in} - I_2^{in}}{I_1^{out} - I_2^{out}})}}{D(I_1^{in} - I_1^{out} - I_2^{in} + I_2^{out})}$$
Deze berekening wordt herhaald op alle gemeten golflengtes.
Met deze waarden kan dan een grafiek geplot worden van $\alpha_\nu$ en $\eta_\nu$ voor helium.
Deze grafiek kunnen we dan verder bespreken.

# Software

De software wordt opgedeeld in meerdere bestand om een overzicht te houden.

## main.py

Dit is het hoofdbestand dat de effectieve analyse zal runnen.

## data_reader.py

Dit bestand zorgt voor het inlezen en herformateren van de data.

### load_data_file(file_path: str, header_row_number: int = 0, delimiter: str = ",", converter_needed: bool = False) -> list:

Laad de data van de OceanView spectrometer software and geeft dit terug in een data matrix.

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

Formatteert de data zodat deze kan gebruikt worden in de analyse.

Args:
    data_matrix_lamp1 (list): The raw data read in by the load_data_file function for lamp 1.
    data_matrix_lamp2 (list): The raw data read in by the load_data_file function for lamp 2.

Raises:
    ValueError: When wavelengths of given data matrices do not correspond.

Returns:
    list: The reformatted data. Structured as [wavelength, lamp_1, lamp_2] for each element.

### seperate_data_lists(data: list) -> tuple: (Unused?)

Splits de data van "reformat_data" in 3 lijsten: golflengtes, lamp 1 intesiteit, lamp 2 intensiteit.

Args:
    data (list): The data matrix obtained by reformatting.

Raises:
    ValueError: When the data has not properly been reformatted.

Returns:
    tuple: A tuple consisting of three lists: wavelength, lamp 1 intensity, lamp 2 intensity

## transfert_vgl.py

Dit bestand berekend de waarden van $\alpha$ en $\eta$.

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

Berekent de functie waarmee de fout op alpha berekend wordt.

Returns:
    callable: Error function for alpha.

### alytical_alpha(I_1_in: float, I_1_out: float, I_2_in: float, I_2_out: float, d: float) -> float:

Berekent de extinctiecoëfficiënt op een bepaalde golflengte.

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

Berekent de functie waarmee de fout op eta berekend wordt.

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

## plotter.py (Unused)

Dit bestand maakt de grafieken aan voor $\alpha_\nu$ en $\eta_\nu$.

## lamp.py

### Class Lamp()

Deze bevat alle data voor een bepaalde lamp. Functies kunnen door gebruik van deze klassen apart gerunt worden per lamp.

#### \__init__(self, lamp_nr: int, voltage: int):

Constructor.

Args:
    lamp_nr (int): The number of the lamp.
    voltage (int): Voltage the lamp was connected to.

Raises:
    ValueError: Voltage is negative.

#### load_in_data(self):

Laad alle data voor de verschillende situates voor deze lamp.

Om deze functie te laten werken is het belangrijk dat de namen van folders en bestanden in ./data/ niet veranderen.

Raises:
    ValueError: If the lamp does not have a valid number.
    ValueError: If a directory does not have the correct name.
    ValueError: If the wavelengths in the data files do not correspond

#### plot_dataset(self, situation: str, fig = None, ax = None, pos1 = None, pos2 = None):

Plot de data voor een bepaalde situatie van deze lamp.

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

Plot de data van alle situaties op één figuur.

Returns:
    plt.fig, plt.ax: The figure and ax objects with all situations plotted.

#### plot_dubbel_data(self):

Plots the data of all situations where a double ballon was used and situations with a single balloon as reference.

Returns:
    plt.fig, plt.ax: The figure and ax objects with described situations plotted.

### main.py

Neergeschreven data van metingen wordt hier ingevuld.
Het programma runt vervolgens de berekeningen uit vorige bestanden.
De bepaalde grafieken worden dan geplot voor de ingegeven lampen.

Met de bepaalde $\eta_{\nu}$ en $\alpha_{\nu}$ wordt de source functie $S_{\nu}$ bepaald en geplot.

### test.py

Wordt gebruikt tijdens het ontwikkelen van de software om functionaliteit te testen zonder te lang te moeten wachten op heel het programma om te runnen.

# Voorbereiding

Het bestand voorbereiding.py is gebruikt om een analytiche oplossing te bepalen voor $\alpha$ en $\eta$ via het stelsel geïntroduceerd aan het begin van de sectie Analyse.
