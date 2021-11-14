![alt text](https://github.com/usnistgov/tb3py/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/usnistgov/tb3py/branch/master/graph/badge.svg?token=TuQF7eVF7F)](https://codecov.io/gh/usnistgov/tb3py)
![alt text](
https://anaconda.org/conda-forge/tb3py/badges/version.svg)
# TB3PY

by Kevin F. Garrity and Kamal Choudhary

This is a python wrapper for the
[ThreeBodyTB.jl](http://github.com/usnistgov/ThreeBodyTB.jl) Julia
package, which runs two- and three-body tight-binding calculations for
materials.

Using the Julia version directly is the primary method for running the
code. However, this code is created to help users who might be more familiar
with python using the
[PyJulia](https://github.com/JuliaPy/pyjulia) interface.

## Installation

First create a conda environment:
Install miniconda environment from https://conda.io/miniconda.html
Based on your system requirements, you'll get a file something like 'Miniconda3-latest-XYZ'.

Now,

```
bash Miniconda3-latest-Linux-x86_64.sh (for linux)
bash Miniconda3-latest-MacOSX-x86_64.sh (for Mac)
```
Download 32/64 bit python 3.6 miniconda exe and install (for windows)
Now, let's make a conda environment, say "version", choose other name as you like::
```
conda create --name my_tb3 python=3.8
source activate my_tb3
conda install -c conda-forge julia
```

Now, let's install the package:
```
pip install requests
git clone https://github.com/usnistgov/tb3py.git
cd tb3py
python setup.py develop
```

Note that this can take a while and may use significant disk space. The code
will, if necessary, a) download & install Julia b) download & install
ThreeBodyTB.jl, and c) create a system image for fast loading.


For main documentation of ThreeBodyTB.jl, see [![](https://img.shields.io/badge/docs-dev-blue.svg)](https://pages.nist.gov/ThreeBodyTB.jl/)
This code is only the wrapper that downloads and installs that code.

Alternate [conda install](https://anaconda.org/conda-forge/tb3py):
```
conda create --name my_tb3 python=3.8
source activate my_tb3
conda install -c conda-forge tb3py
```

## Examples

- Predict total energy, electronic bandgap and bandstructure for a system using POSCAR file:

  ```
  python tb3py/main.py --poscar_file tb3py/examples/POSCAR
  ```
- Predict total energy, electronic bandgap and bandstructure for a system using cif file:

  ```
  python tb3py/main.py --cif_file tb3py/examples/JVASP-1002.cif
  ```

There are several other examples provided to calculate total energies, electronic bandstructures, density of states, forces on atoms, vacancy and surface formation energies in the repo also.
More details and documentation will be available soon.

## Performance Tips

- Julia can take advantage multiple threads. Try setting the environment variable below as appropriate for your machine.
    ```
    JULIA_NUM_THREADS=8
    export JULIA_NUM_THREADS
    ```

- Note that despite using pre-compilation where possible, some
  functions will run faster the second time you run them due to the
  jit.

- Note that you must delete the system image if you want to update the
  ThreeBodyTB.jl code and re-run the installation.

