import tb3py.main as tb3

#this example shows how to use the julia commands directly in python.
#it is also possible to access some of these commands with a more pythonic
#interface using functions defined in main.py

#make crystal object from POSCAR

c = tb3.TB.makecrys("POSCAR")

# calculate energy

#energy, tbc, flag = tb3.TB.scf_energy(c)

# calculate energy force stress

energy, f_cart, stress, tbc = tb3.TB.scf_energy_force_stress(c)

print("PYTHON: energy is ", energy, " eV")
print()
print("PYTHON: force")
print(f_cart)
print()
print("PYTHON: stress")
print(stress)

# All julia commands can be used directly this way, including plotting.
# See https://pages.nist.gov/ThreeBodyTB.jl/ for documenation

#for example 
#tb3.TB.BandStruct.plot_bands(tbc)
