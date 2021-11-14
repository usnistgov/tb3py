"""Module to run tb3py."""

import os
import numpy as np
from julia.api import Julia
from jarvis.core.kpoints import Kpoints3D as Kpoints

# from jarvis.core.kpoints import generate_kgrid

import matplotlib.pyplot as plt
from jarvis.db.figshare import get_jid_data
from jarvis.core.atoms import Atoms
import argparse
import pprint


plt.switch_backend("agg")

# angst_to_bohr = 1  # 0.529177210903  # 1.88973
# const = 13.605662285137

try:
    sysimage = os.path.join(
        os.environ["HOME"], ".julia", "sysimages", "sys_threebodytb.so"
    )
    julia_cmd = "julia"
    # print(os.environ["PATH"])
    jlsession = Julia(
        runtime=julia_cmd, compiled_modules=False, sysimage=sysimage
    )
    jlsession.eval("using Suppressor")  # suppress output
except Exception:
    print("Using non-sysimage version, might be slow.")
    from julia.api import Julia

    jl = Julia(compiled_modules=False)
    cmd = (
        'julia --eval  "using ThreeBodyTB; using Plots; ThreeBodyTB.compile()"'
    )
    os.system(cmd)
    pass
try:
    from julia import ThreeBodyTB as TB
except Exception as exp:
    print("Expjl", exp)
    pass


def get_crys_from_atoms(atoms=None):
    """Get TightlyBound crys object from jarvis.core.Atoms."""
    lattice_mat = np.array(atoms.lattice_mat, dtype="float")
    frac_coords = np.array(atoms.frac_coords, dtype="float")
    elements = np.array(atoms.elements)
    crys = TB.makecrys(lattice_mat, frac_coords, elements)
    return crys


def get_energy_force_stress(atoms=None):
    """Get energy, forces and strss."""
    crys = get_crys_from_atoms(atoms)
    energy, f_cart, stress, tbc = TB.scf_energy_force_stress(crys)
    print("energy, f_cart, stress", energy, f_cart, stress)
    return energy, f_cart, stress, tbc


def get_energy(
    atoms=None, grid=[10, 10, 10], relax_atoms=False, use_grid_for_scf=False
):
    """Get total energy and bandgap."""
    print(atoms)
    info = {}
    energy = "na"
    force = "na"
    stress = "na"

    crys = get_crys_from_atoms(atoms)
    if relax_atoms:
        if use_grid_for_scf:
            cfinal, tbc, energy, force, stress = TB.relax_structure(
                crys, grid=grid
            )
            force = force.tolist()
            stress = stress.tolist()
        else:
            cfinal, tbc, energy, force, stress = TB.relax_structure(crys)
    else:
        if use_grid_for_scf:
            energy, tbc, flag = TB.scf_energy(crys, grid=grid)
        else:
            energy, tbc, flag = TB.scf_energy(crys)
    directgap, indirectgap, gaptype, bandwidth = TB.BandStruct.band_summary(
        tbc
    )
    info["directgap"] = directgap
    info["indirectgap"] = indirectgap
    info["energy"] = energy
    info["force"] = force
    info["stress"] = stress

    return info


def get_energy_bandstructure(atoms=None, filename=None):
    """Get bandstructure, total energy and bandgap."""
    print(atoms)
    kpoints = Kpoints().kpath(atoms, line_density=20)
    labels = kpoints.to_dict()["labels"]
    kpts = kpoints.to_dict()["kpoints"]
    crys = get_crys_from_atoms(atoms)
    energy, tbc, flag = TB.scf_energy(crys)
    tot_energy = energy
    vals = np.array(TB.calc_bands(tbc, kpts) - tbc.efermi)
    vbm, cbm = TB.TB.find_vbm_cbm(vals, tbc.efermi)
    band_gap = cbm - vbm
    if band_gap < 0:
        band_gap = 0
    if filename is not None:
        for i, j in enumerate(vals.T):
            plt.plot(j, c="blue")
        kp = np.arange(len(vals))
        new_kp = []
        new_labels = []
        count = 0

        for i, j in zip(kp, labels):
            if j != "":
                if count > 1 and count < len(labels) - 1:
                    if labels[count] != labels[count + 1]:
                        new_kp.append(i)
                        new_labels.append("$" + str(j) + "$")
                else:
                    new_kp.append(i)
                    new_labels.append("$" + str(j) + "$")
            count += 1
        plt.rcParams.update({"font.size": 18})
        plt.xticks(new_kp, new_labels)
        plt.axhline(y=0, c="g", linestyle="-.")
        plt.ylabel("Energy (eV)")
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        print("Bandstructure plot saved in:", filename)
    return tot_energy, band_gap, tbc


def example():
    """Get an example."""
    A = np.eye(3) * 5.0
    coords = np.zeros((1, 3))
    c = TB.makecrys(A, coords, ["Li"])
    energy, tbc, flag = TB.scf_energy(c)
    return energy, tbc, flag


def predict_for_poscar(filename="POSCAR", band_file="bands.png"):
    """Predict properties for a POSCAR file."""
    atoms = Atoms.from_poscar(filename)
    info = get_energy(atoms=atoms)
    # tot_energy, band_gap, tbc = get_energy_bandstructure(
    #    atoms=atoms, filename=band_file
    # )
    pprint.pprint(info)
    return info


def predict_for_cif(filename="atoms.cif", band_file="bands.png"):
    """Predict properties for a .cif file."""
    try:
        atoms = Atoms.from_cif(filename)
    except Exception as exp:
        raise NotImplementedError("pip install cif2cell, and try again", exp)
        pass
    tot_energy, band_gap, tbc = get_energy_bandstructure(
        atoms=atoms, filename=band_file
    )
    print("tot_energy, band_gap", tot_energy, band_gap)
    return tot_energy, band_gap


def example_from_jarvis_db():
    """Run an example calculation with structure from JARVIS-DFT."""
    atoms = Atoms.from_dict(
        get_jid_data(jid="JVASP-1002", dataset="dft_3d")["atoms"]
    )
    print(atoms)
    tot_energy, band_gap, tbc = get_energy_bandstructure(
        atoms=atoms, filename="bands.png"
    )
    print("tot_energy, band_gap", tot_energy, band_gap)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python wrapper for Tight-binding two and three body."
    )
    # example()
    parser.add_argument(
        "--poscar_file",
        default="NA",
        help="Path to a POSCAR file.",
    )

    parser.add_argument(
        "--cif_file",
        default="NA",
        help="Path to a .cif file.",
    )

    args = parser.parse_args(sys.argv[1:])
    if args.poscar_file != "NA":
        predict_for_poscar(filename=args.poscar_file)
    elif args.cif_file != "NA":
        predict_for_cif(filename=args.cif_file)
    else:
        raise NotImplementedError(args)
