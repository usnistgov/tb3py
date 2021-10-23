"""Predict properties of a db."""

from jarvis.db.figshare import data
from jarvis.db.jsonutils import dumpjson
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from jarvis.core.atoms import Atoms
from tb3py.main import get_energy

plt.switch_backend("agg")


def predict_for_db(
    dataset="dft_3d",
    id_tag="jid",
    gap_key="optb88vdw_bandgap",
    energy_key="optb88vdw_total_energy",
):
    """Predict values for a DB."""
    d = data(dataset)
    mem = []

    for ii, i in enumerate(d):
        # if ii < 5:
        try:
            a = Atoms.from_dict(i["atoms"])
            info = get_energy(a)
            info["id"] = i[id_tag]
            if gap_key != "":
                info[dataset + "_" + gap_key] = i[gap_key]
            if energy_key != "":
                info[dataset + "_" + energy_key] = i[energy_key]
            mem.append(info)
        except Exception as exp:
            print(exp)
            pass
    dumpjson(data=mem, filename=dataset + "_tb.json")

    if gap_key != "":
        mae_gap = mean_absolute_error(
            [i[dataset + "_" + gap_key] for i in mem],
            [i["indirectgap"] for i in mem],
        )
        plt.plot(
            [i[dataset + "_" + gap_key] for i in mem],
            [i["indirectgap"] for i in mem],
            ".",
        )
        plt.plot(
            [i[dataset + "_" + gap_key] for i in mem],
            [i[dataset + "_" + gap_key] for i in mem],
        )
        name = dataset + "_" + gap_key + ".png"
        plt.savefig(name)
        plt.close()
        print("mae_gap", mae_gap)
    if energy_key != "":
        mae_energy = mean_absolute_error(
            [i[dataset + "_" + energy_key] for i in mem],
            [i["energy"] for i in mem],
        )
        plt.plot(
            [i[dataset + "_" + energy_key] for i in mem],
            [i["energy"] for i in mem],
            ".",
        )
        plt.plot(
            [i[dataset + "_" + energy_key] for i in mem],
            [i[dataset + "_" + energy_key] for i in mem],
        )
        name = dataset + "_" + energy_key + ".png"
        plt.savefig(name)
        plt.close()
        print("mae_energy", mae_energy)


if __name__ == "__main__":
    predict_for_db()
