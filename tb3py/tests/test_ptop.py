from tb3py.main import example, get_energy_bandstructure


def test_example():
    energy, tbc, flag = example()
    print(energy)
    assert round(energy, 5) == round(-0.43160184930052803, 5)


def test_jarvis_dat():
    from jarvis.db.figshare import get_jid_data
    from jarvis.core.atoms import Atoms

    atoms = Atoms.from_dict(
        get_jid_data(jid="JVASP-664", dataset="dft_2d")["atoms"]
    )
    get_energy_bandstructure(atoms=atoms)


# test_example()
