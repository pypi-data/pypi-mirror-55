"""Module for liquid water content calculations."""

import numpy as np
import cloudnetpy.constants as con


def adiabatic_lwc(T, P):
    """Returns adiabatic LWC change rate.

    Calculates the theoretical adiabatic rate of increase of LWC with
    height, or pressure, given the cloud base temperature and pressure.

    Args:
        T (ndarray): Temperature of cloud base (K).
        P (ndarray): Pressure of cloud base (Pa).

    Returns:
        ndarray: dlwc/dz in kg m-3 m-1

    References:
        Brenguier, 1991, https://bit.ly/2QCSJtb

    """
    e = con.MW_RATIO
    g = con.g
    cp = con.SPECIFIC_HEAT
    L = con.LATENT_HEAT
    R = con.RS

    qs, es = temp2mixingratio(T, P)
    rhoa = P / (R*T*(0.6*qs + 1))
    a, b = cp*T/(L*e), P-es
    f1 = -1 + a
    f2 = 1/(a + (L*qs*rhoa/b))
    f3 = rhoa*g*e*es*b**-2
    return rhoa*f1*f2*f3


def temp2mixingratio(T, P):
    """Converts temperature and pressure to mixing ratio.

    Args:
        T (ndarray): Temperature (K).
        P (ndarray): Pressure (Pa).

    Returns:
        ndarray: Mixing ratio.

    """
    t1 = T/con.T0
    t2 = 1 - (con.T0/T)
    svp = 10**(10.79574*t2-5.028*np.log10(t1)
               + 1.50475e-4*(1-(10**(-8.2969*(t1-1))))
               + 0.42873e-3*(10**(4.76955*t2))
               + 2.78614)
    mixing_ratio = con.MW_RATIO * svp / (P - svp)
    return mixing_ratio, svp
