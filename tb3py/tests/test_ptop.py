from tb3py.main import example


def test_example():
    energy, tbc, flag = example()
    print(energy)
    assert round(energy, 5) == round(-0.43160184930052803, 5)


test_example()
