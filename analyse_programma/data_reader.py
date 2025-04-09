import numpy as np
"""
This library contains functions to read the data files from the OceanView software for the spectrometer and to reformat the data.

TODO:
    Finish documentation in README
    update documentation
"""


def load_data_file(file_path: str, header_row_number: int = 0, delimiter: str = ",", converter_needed: bool = False):
    """
    Loads one data file and returns the content as a matrix.

    Args:
        file_path (str): The directory path to the file including the filename.
        header_row_number (int, optional): The amount of rows the header takes up. Defaults to 0.
        delimiter (str, optional): The character seperating the values in the data file. Defaults to ",".
        converter_needed (bool, optional): Whether or not the data files need commas to be replaced with decimal points. Defaults to False.

    Returns:
        list: The raw data contained in a matrix.
    """
    if converter_needed == True:
        golf, intens = np.loadtxt(file_path,
                            delimiter=delimiter,
                            skiprows=header_row_number,
                            converters=lambda s: s.replace(',', '.'),
                            unpack=True)
    else:
        golf, intens = np.loadtxt(file_path,
                          delimiter=delimiter,
                          skiprows=header_row_number,
                          unpack=True)

    return golf, intens


def reformat_data(data_matrix_lamp1: list, data_matrix_lamp2: list) -> list:
    """
    Reformats data to be able to use in further analysis.

    Args:
        data_matrix_lamp1 (list): The raw data read in by the load_data_file function for lamp 1.
        data_matrix_lamp2 (list): The raw data read in by the load_data_file function for lamp 2.

    Raises:
        ValueError: When wavelengths of given data matrices do not correspond.

    Returns:
        list: The reformatted data. Structured as [wavelength, lamp_1, lamp_2] for each element.
    """
    reformatted_data = []

    for data_1, data_2 in zip(data_matrix_lamp1, data_matrix_lamp2):

        if data_1[0] == data_2[0]:
            reformatted_data.append([data_1[0], data_1[1], data_2[1]])

        else:
            raise ValueError("Wavelengths do not correspond")
        
    return reformatted_data


def seperate_data_lists(data: list) -> tuple:
    """
    Seperates the data from reformat_data into three lists: wavelength, lamp 1, lamp 2

    Args:
        data (list): The data matrix obtained by reformatting.

    Raises:
        ValueError: When the data has not properly been reformatted.

    Returns:
        tuple: A tuple consisting of three lists: wavelength, lamp 1 intensity, lamp 2 intensity
    """
    if len(data[0]) != 3:
        raise ValueError("Data has not been reformatted properly")
    
    wavlens = []
    lamp1 = []
    lamp2 = []

    for i in range(0, len(data)):
        wavlens.append(data[i][0])
        lamp1.append(data[i][1])
        lamp2.appnd(data[i][2])

    return wavlens, lamp1, lamp2