# from jarvis.analysis.defects.vacancy import Vacancy
from jarvis.db.jsonutils import dumpjson
from jarvis.core.atoms import Atoms
from jarvis.db.figshare import get_jid_data, data
from tb3py.main import get_energy
# from jarvis.analysis.thermodynamics.energetics import get_optb88vdw_energy
from jarvis.analysis.structure.spacegroup import (
    Spacegroup3D,
    symmetrically_distinct_miller_indices,
)
from jarvis.analysis.defects.surface import Surface
import numpy as np

dat = data("dft_3d")


# x = get_optb88vdw_energy()
# jids_elements = [i["jid"] for i in x.values()]


jids = ["JVASP-14971"]
# chempot_maker1.py
jids = ["JVASP-867"]  # Cu
jids = ["JVASP-32"]  # Al2O3
jids = [
    "JVASP-816",
    "JVASP-910",
    "JVASP-867",
    "JVASP-922",
    "JVASP-21195",
    "JVASP-1002",
    "JVASP-972",
    "JVASP-943",
    "JVASP-852",
    "JVASP-890",
    "JVASP-922",
    "JVASP-987",
    "JVASP-14832",
    "JVASP-14837",
    "JVASP-14622",
    "JVASP-14744",
    "JVASP-14812",
    "JVASP-14812",
    "JVASP-14601",
    "JVASP-14603",
    "JVASP-14604",
    "JVASP-14606",
    "JVASP-14612",
    "JVASP-14725",
    "JVASP-88846",
    "JVASP-7804",
    "JVASP-858",
    "JVASP-79561",
    "JVASP-828",
    "JVASP-25104",
    "JVASP-25144",
    "JVASP-919",
    "JVASP-25273",
    "JVASP-916",
    "JVASP-1035",
    "JVASP-25254",
    "JVASP-25250",
    "JVASP-25248",
    "JVASP-25142",
    "JVASP-949",
    "JVASP-949",
    "JVASP-25213",
    "JVASP-937",
    "JVASP-937",
    "JVASP-25210",
    "JVASP-25407",
    "JVASP-25407",
    "JVASP-1017",
    "JVASP-1017",
    "JVASP-946",
    "JVASP-1020",
    "JVASP-1050",
    "JVASP-21197",
    "JVASP-25388",
    "JVASP-1014",
    "JVASP-958",
    "JVASP-25180",
    "JVASP-25379",
    "JVASP-25125",
    "JVASP-25125",
    "JVASP-870",
    "JVASP-870",
    "JVASP-993",
    "JVASP-802",
    "JVASP-21193",
    "JVASP-901",
    "JVASP-25117",
    "JVASP-25117",
    "JVASP-861",
    "JVASP-931",
    "JVASP-25114",
    "JVASP-981",
    "JVASP-834",
    "JVASP-33718",
    "JVASP-966",
    "JVASP-966",
    "JVASP-810",
    "JVASP-810",
    "JVASP-898",
    "JVASP-25337",
    "JVASP-825",
    "JVASP-837",
    "JVASP-1056",
    "JVASP-969",
    "JVASP-969",
    "JVASP-961",
    "JVASP-1011",
    "JVASP-895",
    "JVASP-934",
    "JVASP-840",
    "JVASP-984",
    "JVASP-819",
    "JVASP-25167",
    "JVASP-1029",
    "JVASP-1029",
    "JVASP-996",
    "JVASP-910",
    "JVASP-963",
    "JVASP-922",
    "JVASP-1026",
    "JVASP-95268",
    "JVASP-102277",
    "JVASP-102277",
]

jids = [
    "JVASP-972",
    "JVASP-825",
    "JVASP-1002",
    "JVASP-943",
    "JVASP-963",
    "JVASP-14606",
    "JVASP-14837",
    "JVASP-934",
    "JVASP-21195",
    "JVASP-984",
    "JVASP-1014",
    "JVASP-79561",
    "JVASP-901",
]


def get_mono_surf_energy(atoms=None, id=""):
    atoms_cvn = Spacegroup3D(atoms).conventional_standard_structure
    info_perfect = get_energy(atoms_cvn, relax_atoms=False)
    indices = symmetrically_distinct_miller_indices(
        max_index=1, cvn_atoms=atoms_cvn
    )

    epa = info_perfect["energy"] / atoms_cvn.num_atoms
    mem = []
    for j in indices:
        strt = Surface(atoms=atoms_cvn, indices=j).make_surface()
        print(strt)
        print(j)
        name = (
            id
            + "_"
            + str(strt.composition.reduced_formula)
            + "_"
            + str("_".join(map(str, j)))
        )

        info_def = get_energy(strt, relax_atoms=False)
        m = np.array(strt.lattice_mat)
        surf_area = np.linalg.norm(np.cross(m[0], m[1]))
        surf_en = (
            16
            * (info_def["energy"] - epa * (strt.num_atoms))
            / (2 * surf_area)
        )

        print("Surface name", name, surf_en)
        info = {}
        info["name"] = name
        info["surf_en"] = surf_en
        info["energy"] = info_def["energy"]
        info["perf_atoms"] = info_perfect  # .to_dict()
        info["defect_atoms"] = strt.to_dict()
        fname = name + ".json"
        dumpjson(filename=fname, data=info)
        mem.append(info)

        # return name, def_en,epa
    return mem


mem = []
for i in jids:
    try:
        atoms = Atoms.from_dict(get_jid_data(jid=i, dataset="dft_3d")["atoms"])
        print("STARTING")
        print("jid", i)
        print(atoms)
        dinfo = get_mono_surf_energy(atoms=atoms, id=i)
        # nm, def_en,epa = get_mono_vac_energy(atoms=atoms)
        info = {}
        info["id"] = i
        info["defect_energetics"] = dinfo
        mem.append(info)
        print("NAME", len(mem), i, mem[-1])
    except Exception as exp:
        print("Exp", exp)
        pass

print("mem", len(mem))
dumpjson(data=mem, filename="mono_surf2multi-Elements.json")
