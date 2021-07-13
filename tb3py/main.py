"""Module to run tb3py."""

import os
from julia.api import Julia
sysimage = os.path.join(
    os.environ["HOME"], ".julia", "sysimages", "sys_threebodytb.so"
)
julia_cmd = mpath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "julia",
    "julia-1.6.1",
    "bin",
    "julia",
)


jlsession = Julia(runtime=julia_cmd, compiled_modules=False, sysimage=sysimage)
jlsession.eval("using Suppressor")  # suppress output


def get_module():
    """Get module."""
    from julia import TightlyBound as TB

    return TB


def example():
    """Get module."""
    from julia import ThreeBodyTB as TB3

    # import TB3

    import numpy as np

    A = np.eye(3) * 5.0
    coords = np.zeros((1, 3))
    c = TB3.makecrys(A, coords, ["Li"])
    energy, tbc, flag = TB3.scf_energy(c)
