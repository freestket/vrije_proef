import numpy as np
import sympy as sp
from lamp import Lamp
import matplotlib.pyplot as plt
"""
This library contains functions to calculate alpha and eta as well as a the general solution to the radiation transfer equation.
"""


def general_transfer_solution(I_in, alpha, eta, d):
    """
    Gives the outgoing intensity from the general solution of the radiation transfer equation.

    Args:
        I_in (_type_): Ingoing intensity.
        alpha (_type_): Extinction coefficient.
        eta (_type_): Emission coefficient.
        d (_type_): Distance traveled by radiation.

    Returns:
        _type_: Outgoing intensity.
    """
    I_out = I_in*np.exp(-alpha*d) + (eta/alpha)*(1-np.exp(-alpha*d))
    return I_out


def analytical_alpha_error():
    """
    Calculates the lambdified error function for alpha.

    Returns:
        callable: Error function for alpha.
    """
    I1_in, I1_out, I2_in, I2_out, alpha, eta, D = sp.symbols('I_1^in I_1^out I_2^in I_2^out alpha eta D')

    sol = sp.solve([I1_out - I1_in*sp.exp(-alpha*D) - eta/alpha*(1-sp.exp(-alpha*D)),
                I2_out - I2_in*sp.exp(-alpha*D) - eta/alpha*(1-sp.exp(-alpha*D))],
                [alpha, eta])
    
    alpha_sympy = sol[0][0]

    sI1_in, sI1_out, sI2_in, sI2_out, sD = sp.symbols('s_{I_1^in} s_{I_1^out} s_{I_2^in} s_{I_2^out} s_D')

    alpha_err_sympy = sp.simplify(sp.sqrt(
                          sp.diff(alpha_sympy, I1_in)**2*sI1_in**2
                        + sp.diff(alpha_sympy, I1_out)**2*sI1_out**2
                        + sp.diff(alpha_sympy, I2_in)**2*sI2_in**2
                        + sp.diff(alpha_sympy, I2_out)**2*sI2_out**2
                        + sp.diff(alpha_sympy, D)**2*sD**2))
    
    f_alpha_err = sp.lambdify([I1_in, I1_out, I2_in, I2_out, D, sI1_in, sI1_out, sI2_in, sI2_out, sD], alpha_err_sympy)

    return f_alpha_err


def analytical_alpha(I_1_in: float, I_1_out: float, I_2_in: float, I_2_out: float, d: float,
                     I_1_in_err: float, I_1_out_err: float, I_2_in_err: float, I_2_out_err: float, d_err: float,
                     error_function) -> float:
    """
    Calculates the extinction coefficient on a certain wavelength.

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
        float: The extinction coefficient on a given wavelength
        float: Error on the extinction coefficient.
    """
    alpha = np.log( (I_1_in - I_2_in) / (I_1_out - I_2_out) ) / d

    alpha_err = error_function(I_1_in, I_1_out, I_2_in, I_2_out, d, I_1_in_err, I_1_out_err, I_2_in_err, I_2_out_err, d_err)

    return alpha, alpha_err


def analytical_eta_error():
    """
    Calculates the lambdified error function for eta.

    Returns:
        callable: Error function for eta.
    """
    I1_in, I1_out, I2_in, I2_out, alpha, eta, D = sp.symbols('I_1^in I_1^out I_2^in I_2^out alpha eta D')

    sol = sp.solve([I1_out - I1_in*sp.exp(-alpha*D) - eta/alpha*(1-sp.exp(-alpha*D)),
                I2_out - I2_in*sp.exp(-alpha*D) - eta/alpha*(1-sp.exp(-alpha*D))],
                [alpha, eta])
    
    eta_sympy = sol[0][1]

    sI1_in, sI1_out, sI2_in, sI2_out, sD = sp.symbols('s_{I_1^in} s_{I_1^out} s_{I_2^in} s_{I_2^out} s_D')

    eta_err_sympy = sp.simplify(sp.sqrt(
                          sp.diff(eta_sympy, I1_in)**2*sI1_in**2
                        + sp.diff(eta_sympy, I1_out)**2*sI1_out**2
                        + sp.diff(eta_sympy, I2_in)**2*sI2_in**2
                        + sp.diff(eta_sympy, I2_out)**2*sI2_out**2
                        + sp.diff(eta_sympy, D)**2*sD**2))
    
    f_eta_err = sp.lambdify([I1_in, I1_out, I2_in, I2_out, D, sI1_in, sI1_out, sI2_in, sI2_out, sD], eta_err_sympy)

    return f_eta_err


def analytical_eta(I_1_in: float, I_1_out: float, I_2_in: float, I_2_out: float, d: float, 
                   I_1_in_err: float, I_1_out_err:float, I_2_in_err:float, I_2_out_err:float, d_err:float,
                   error_function) -> float:
    """
    Calculates the emission coefficient on a certain wavelength.

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
    """

    eta = (I_1_in*I_2_out - I_1_out*I_2_in) * np.log( (I_1_in - I_2_in) / (I_1_out - I_2_out) ) / ( d*(I_1_in - I_1_out - I_2_in + I_2_out) )

    
    eta_err = error_function(I_1_in, I_1_out, I_2_in, I_2_out, d, I_1_in_err, I_1_out_err, I_2_in_err, I_2_out_err, d_err)

    return eta, eta_err


def calculate_alpha_eta(lamp1 : Lamp, lamp2: Lamp, D: float, d_err: float, pure_helium: bool = False, no_ballon_bck: bool = False):
    """
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
    """
    lamp1.load_in_data()
    lamp2.load_in_data()

    if no_ballon_bck:
        golf_l1 = lamp1.bck_noballon_data[0]
        golf_l1_err = lamp1.bck_noballon_data_err[0]

        incoming_I_l1 = lamp1.bck_noballon_data[1]
        incoming_I_l1_err = lamp1.bck_noballon_data_err[1]

        incoming_I_l2 = lamp2.bck_noballon_data[1]
        incoming_I_l2_err = lamp2.bck_noballon_data_err[1]

        ballon = "no balloon"

    else:
        golf_l1 = lamp1.bck_data[0]
        golf_l1_err = lamp1.bck_data_err[0]

        incoming_I_l1 = lamp1.bck_data[1]
        incoming_I_l1_err = lamp1.bck_data_err[1]

        incoming_I_l2 = lamp2.bck_data[1]
        incoming_I_l2_err = lamp2.bck_data_err[1]

        ballon = "a balloon filled with air"


    if pure_helium:
        outgoing_I_l1 = lamp1.helium_sterk_data[1]
        outgoing_I_l1_err = lamp1.helium_sterk_data_err[1]

        outgoing_I_l2 = lamp2.helium_sterk_data[1]
        outgoing_I_l2_err = lamp2.helium_sterk_data_err[1]

        hel = "pure"

    else:
        outgoing_I_l1 = lamp1.helium_zwak_data[1]
        outgoing_I_l1_err = lamp1.helium_zwak_data_err[1]

        outgoing_I_l2 = lamp2.helium_zwak_data[1]
        outgoing_I_l2_err = lamp2.helium_zwak_data_err[1]

        hel = "commercial"



    alpha_nu = []
    alpha_nu_err = []
    eta_nu = []
    eta_nu_err = []

    alpha_error_func = analytical_alpha_error()
    eta_error_func = analytical_eta_error()

    for i in range(0, len(golf_l1)):
        alpha, alpha_err = analytical_alpha(incoming_I_l1[i], outgoing_I_l1[i],
                                            incoming_I_l2[i], outgoing_I_l2[i],
                                            D, 
                                            incoming_I_l1_err[i], outgoing_I_l1_err[i],
                                            incoming_I_l2_err[i], outgoing_I_l2_err[i],
                                            d_err,
                                            alpha_error_func)
        eta, eta_err = analytical_eta(incoming_I_l1[i], outgoing_I_l1[i],
                                        incoming_I_l2[i], outgoing_I_l2[i],
                                        D, 
                                        incoming_I_l1_err[i], outgoing_I_l1_err[i],
                                        incoming_I_l2_err[i], outgoing_I_l2_err[i],
                                        d_err,
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

    fig.suptitle(f"Coëfficients for {hel} helium, using {ballon} in incoming radiation measurements", fontsize=16)

    return fig, ax, golf, alpha_nu, alpha_nu_err, eta_nu, eta_nu_err