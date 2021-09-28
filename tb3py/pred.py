"""Predict properties of a db."""
from jarvis.db.figshare import data
from sklearn.metrics import mean_absolute_error

d = data("qe_tb")
from jarvis.core.atoms import Atoms
from tb3py.main import get_energy_bandstructure, get_energy
from jarvis.core.atoms import Atoms

tb_vals = []
dft_vals = []
gap_key = "indir_gap"
for i in d:
    a = Atoms.from_dict(i["atoms"])
    info = get_energy(a)
    # tot_energy, band_gap, tbc=get_energy_bandstructure(a)
    print("TB gap, DFT gap", info["indirectgap"], i["indir_gap"])
    tb_vals.append(info["indirectgap"])
    dft_vals.append(i["indir_gap"])
    # break
mae = mean_absolute_error(dft_vals, tb_vals)
print(mae)
