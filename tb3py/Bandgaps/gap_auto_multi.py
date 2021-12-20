"""Module for vacancy formation energy."""

# from jarvis.analysis.defects.vacancy import Vacancy
from jarvis.db.jsonutils import dumpjson
from jarvis.core.atoms import Atoms
from jarvis.db.figshare import data
from tb3py.main import get_energy

# from jarvis.analysis.thermodynamics.energetics import get_optb88vdw_energy

dat = data("dft_3d")


# x = get_optb88vdw_energy()
# jids_elements = [i["jid"] for i in x.values()]


jids = [
    "JVASP-91",
    "JVASP-1002",
    "JVASP-890",
    "JVASP-17",
    "JVASP-39",
    "JVASP-7844",
    "JVASP-30",
    "JVASP-8169",
    "JVASP-1180",
    "JVASP-1312",
    "JVASP-1393",
    "JVASP-1327",
    "JVASP-1183",
    "JVASP-1408",
    "JVASP-1189",
    "JVASP-1174",
    "JVASP-97",
    "JVASP-7630",
    "JVASP-54",
    "JVASP-57",
    "JVASP-72",
    "JVASP-75",
    "JVASP-32",
    "JVASP-23",
    "JVASP-7860",
    "JVASP-299",
    "JVASP-116",
    "JVASP-1405",
    "JVASP-95",
    "JVASP-8003",
    "JVASP-1192",
    "JVASP-1300",
    "JVASP-7678",
    "JVASP-7762",
    "JVASP-1315",
    "JVASP-1294",
    "JVASP-1267",
    "JVASP-5",
    "JVASP-104",
    "JVASP-1216",
    "JVASP-1453",
    "JVASP-113",
    "JVASP-9147",
    "JVASP-1201",
    "JVASP-8082",
    "JVASP-1702",
    "JVASP-96",
    "JVASP-1198",
    "JVASP-8158",
    "JVASP-1130",
    "JVASP-1145",
    "JVASP-1954",
    "JVASP-8583",
    "JVASP-8566",
]

# chempot = loadjson("chempot.json")


def get_gap(atoms=None, jid=""):
    """Get vacancy formation energy."""

    name = str(jid) + "_" + str(atoms.composition.reduced_formula)

    info_def = get_energy(atoms, relax_atoms=False)
    fname = name + ".json"
    dumpjson(data=info_def, filename=fname)
    return info_def


mem = []
for i in dat:
    if i["jid"] in jids:
        # try:
        atoms = Atoms.from_dict(i["atoms"])
        print("STARTING")
        print("jid", i["jid"])
        print(atoms)
        dinfo = get_gap(atoms=atoms, jid=i["jid"])
        # nm, def_en,epa = get_mono_vac_energy(atoms=atoms)
        info = {}
        info["id"] = i["jid"]
        info["defect_energetics"] = dinfo
        mem.append(info)
        print("NAME", len(mem), i["jid"], mem[-1])
    # except Exception as exp:
    #    print("Exp", exp)
    #    pass

print("mem", len(mem))
dumpjson(data=mem, filename="mono_vac2multi-Elements.json")
