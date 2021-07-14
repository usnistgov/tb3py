"""Module to run tb3py."""
import numpy as np
import os


def get_module():
    """Get module."""
    from julia import TightlyBound as TB

    return TB


def example():
    """Get module."""
    from julia import ThreeBodyTB as TB3

    # import TB3

    A = np.eye(3) * 5.0
    coords = np.zeros((1, 3))
    c = TB3.makecrys(A, coords, ["Li"])
    energy, tbc, flag = TB3.scf_energy(c)
