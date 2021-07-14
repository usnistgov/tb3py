"""Module to run tb3py."""
import numpy as np
from jarvis.core.kpoints import Kpoints3D as Kpoints
from julia import ThreeBodyTB as TB
import matplotlib.pyplot as plt

plt.switch_backend("agg")

angst_to_bohr = 1.88973
const = 13.605662285137


def get_crys_from_atoms(atoms=None):
    """Get TightlyBound crys object from jarvis.core.Atoms."""
    lattice_mat = np.array(atoms.lattice_mat, dtype="float") * angst_to_bohr
    frac_coords = np.array(atoms.frac_coords, dtype="float")
    elements = np.array(mat.elements)
    crys = TB.makecrys(lattice_mat, frac_coords, elements)
    return crys


def get_energy_bandstructure(atoms=None, filename=None):
    kpoints = Kpoints().kpath(atoms, line_density=20)
    labels = kpoints.to_dict()["labels"]
    kpts = kpoints.to_dict()["kpoints"]
    crys = get_crys_from_atoms(atoms)
    energy, tbc, flag = TB.scf_energy(crys)
    tot_energy = round(const * float(energy), 5)
    vals = const * np.array(B.calc_bands(tbc, kpts) - tbc.efermi)
    vbm, cbm = TB.TB.find_vbm_cbm(vals, const * tbc.efermi)
    band_gap = cbm - vbm
    if band_gap < 0:
        bandg_gap = 0
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
        plt.xticks(new_kp, new_labels)
        plt.ylabel("Energy (eV)")
        plt.savefig(filename)
        plt.close()
    return tot_energy, band_gap


def example():
    """Get an example."""
    A = np.eye(3) * 5.0
    coords = np.zeros((1, 3))
    c = TB.makecrys(A, coords, ["Li"])
    energy, tbc, flag = TB.scf_energy(c)
    return energy, tbc, flag


if __name__ == "__main__":
    from jarvis.db.figshare import get_jid_data
    from jarvis.core.atoms import Atoms

    atoms = Atoms.from_dict(
        get_jid_data(jid="JVASP-1002", dataset="dft_3d")["atoms"]
    )
    get_energy_bandstructure(atoms=atoms)
