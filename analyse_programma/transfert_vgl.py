import numpy as np
import sympy as sp
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