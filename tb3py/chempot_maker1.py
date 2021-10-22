from jarvis.analysis.defects.vacancy import Vacancy
from jarvis.db.jsonutils import loadjson,dumpjson
from jarvis.core.atoms import Atoms
from jarvis.db.figshare import data
from tb3py.main import get_energy_bandstructure, get_energy
from jarvis.analysis.thermodynamics.energetics import get_optb88vdw_energy

dat = data("dft_3d")


#x = get_optb88vdw_energy()
#jids_elements = [i["jid"] for i in x.values()]

jids=['JVASP-910', 'JVASP-867', 'JVASP-922', 'JVASP-21195', 'JVASP-1002', 'JVASP-816', 'JVASP-972', 'JVASP-943', 'JVASP-852', 'JVASP-890', 'JVASP-922', 'JVASP-987', 'JVASP-14832', 'JVASP-14837', 'JVASP-14622', 'JVASP-14744', 'JVASP-14812', 'JVASP-14812', 'JVASP-14601', 'JVASP-14603', 'JVASP-14604', 'JVASP-14606', 'JVASP-14612', 'JVASP-14725', 'JVASP-88846', 'JVASP-7804', 'JVASP-858', 'JVASP-79561', 'JVASP-828', 'JVASP-25104', 'JVASP-25144', 'JVASP-919', 'JVASP-25273', 'JVASP-916', 'JVASP-1035', 'JVASP-25254', 'JVASP-25250', 'JVASP-25248', 'JVASP-25142', 'JVASP-949', 'JVASP-949', 'JVASP-25213', 'JVASP-937', 'JVASP-937', 'JVASP-25210', 'JVASP-25407', 'JVASP-25407', 'JVASP-1017', 'JVASP-1017', 'JVASP-946', 'JVASP-1020', 'JVASP-1050', 'JVASP-21197', 'JVASP-25388', 'JVASP-1014', 'JVASP-958', 'JVASP-25180', 'JVASP-25379', 'JVASP-25125', 'JVASP-25125', 'JVASP-870', 'JVASP-870', 'JVASP-993', 'JVASP-802', 'JVASP-21193', 'JVASP-901', 'JVASP-25117', 'JVASP-25117', 'JVASP-861', 'JVASP-931', 'JVASP-25114', 'JVASP-981', 'JVASP-834', 'JVASP-33718', 'JVASP-966', 'JVASP-966', 'JVASP-810', 'JVASP-810', 'JVASP-898', 'JVASP-25337', 'JVASP-825', 'JVASP-837', 'JVASP-1056', 'JVASP-969', 'JVASP-969', 'JVASP-961', 'JVASP-1011', 'JVASP-895', 'JVASP-934', 'JVASP-840', 'JVASP-984', 'JVASP-819', 'JVASP-25167', 'JVASP-1029', 'JVASP-1029', 'JVASP-996', 'JVASP-910', 'JVASP-963', 'JVASP-922', 'JVASP-1026', 'JVASP-95268', 'JVASP-102277', 'JVASP-102277']


jids_els=['JVASP-910', 'JVASP-867', 'JVASP-922', 'JVASP-21195', 'JVASP-1002', 'JVASP-816', 'JVASP-972', 'JVASP-943', 'JVASP-852', 'JVASP-890', 'JVASP-922', 'JVASP-987', 'JVASP-14832', 'JVASP-14837', 'JVASP-14622', 'JVASP-14744', 'JVASP-14812', 'JVASP-14812', 'JVASP-14601', 'JVASP-14603', 'JVASP-14604', 'JVASP-14606', 'JVASP-14612', 'JVASP-14725', 'JVASP-88846', 'JVASP-7804', 'JVASP-858', 'JVASP-79561', 'JVASP-828', 'JVASP-25104', 'JVASP-25144', 'JVASP-919', 'JVASP-25273', 'JVASP-916', 'JVASP-1035', 'JVASP-25254', 'JVASP-25250', 'JVASP-25248', 'JVASP-25142', 'JVASP-949', 'JVASP-949', 'JVASP-25213', 'JVASP-937', 'JVASP-937', 'JVASP-25210', 'JVASP-25407', 'JVASP-25407', 'JVASP-1017', 'JVASP-1017', 'JVASP-946', 'JVASP-1020', 'JVASP-1050', 'JVASP-21197', 'JVASP-25388', 'JVASP-1014', 'JVASP-958', 'JVASP-25180', 'JVASP-25379', 'JVASP-25125', 'JVASP-25125', 'JVASP-870', 'JVASP-870', 'JVASP-993', 'JVASP-802', 'JVASP-21193', 'JVASP-901', 'JVASP-25117', 'JVASP-25117', 'JVASP-861', 'JVASP-931', 'JVASP-25114', 'JVASP-981', 'JVASP-834', 'JVASP-33718', 'JVASP-966', 'JVASP-966', 'JVASP-810', 'JVASP-810', 'JVASP-898', 'JVASP-25337', 'JVASP-825', 'JVASP-837', 'JVASP-1056', 'JVASP-969', 'JVASP-969', 'JVASP-961', 'JVASP-1011', 'JVASP-895', 'JVASP-934', 'JVASP-840', 'JVASP-984', 'JVASP-819', 'JVASP-25167', 'JVASP-1029', 'JVASP-1029', 'JVASP-996', 'JVASP-910', 'JVASP-963', 'JVASP-922', 'JVASP-1026', 'JVASP-95268', 'JVASP-102277', 'JVASP-102277']



from collections import defaultdict
mem = defaultdict()
for i in dat:
    if i["jid"] in jids_els:
        try:
            atoms = Atoms.from_dict(i["atoms"])
            print("STARTING")
            print("jid", i["jid"])
            print(atoms)
            info_perfect = get_energy(atoms,relax_atoms=False)

            epa = info_perfect["energy"] / atoms.num_atoms

            mem[atoms.elements[0]]={'jid':i['jid'],'energy':epa}
            print("NAME", len(mem), mem)
        except Exception as exp:
            print("Exp", exp)
            pass

print("mem", len(mem))
dumpjson(data=mem, filename="chempot.json")