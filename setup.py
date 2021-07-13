#!/usr/bin/python3
import os
import sys
import subprocess

# import requests
import glob
import os

from setuptools import setup, find_packages

# TB3_DIR = os.path.dirname(os.path.abspath(__file__))

base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "README.md")) as f:
    long_d = f.read()


def precompile(julia=None):
    """Precompile Julia"""
    print("precompile")
    if julia is None:
        julia = "julia"  # julia command
    #    os.system(julia+" --eval  \"using TightlyBound; TightlyBound.compile()\"")
    os.system(
        julia
        + ' --eval  "using ThreeBodyTB; using Plots; ThreeBodyTB.compile()"'
    )


def install(julia=None):
    """Install Julia and TB"""
    if julia is None:
        julia = "julia"  # julia command
    print("install ", julia)
    #    os.system(julia+" --eval "+"\"import Pkg; Pkg.add(url=\\\"https://github.com/kfgarrity/ThreeBodyTB.jl\\\")\"")

    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"ThreeBodyTB\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"PyCall\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"Plots\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"Suppressor\\")"')
    precompile(julia)


setup(
    name="tb3py",
    version="2021.07.10",
    long_description=long_d,
    install_requires=[
        "requests>=2.26.0",
        "numpy>=1.19.5",
        "julia>=0.5.6",
    ],
    extras_require={
        "jarvis-tools": ["jarvis-tools"],
    },
    author="Kevin Garrity, Kamal Choudhary",
    author_email="kevin.garrity@nist.gov",
    description=(
        "tb3: an open-source software package for accurate and efficient electronic structure calculations using tight-binding (TB), including three-body interactions. https://pages.nist.gov/ThreeBodyTB.jl"
    ),
    license="NIST",
    url="https://github.com/kfgarrity/ThreeBodyTB_python",
    packages=find_packages(),
    # long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    # scripts=glob.glob(os.path.join(JARVIS_DIR,  "*"))
)


mpath = os.path.dirname(os.path.realpath(__file__))


# main path
try:
    out, err = subprocess.Popen(
        ["julia", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).communicate()
except:
    out = ""
# check if JUlia has the correct version
hasjulia = (
    ("julia version 1.6" in str(out))
    or ("julia version 1.5" in str(out))
    or ("julia version 1.7" in str(out))
    or ("julia version 1.8" in str(out))
)


# print(hasjulia) ; exit()

print("hasjulia: ", hasjulia)

if not hasjulia:  # if the correct Julia version is not present
    julia_cmd = os.path.join(
        mpath, "tb3py", "julia", "julia-1.6.1", "bin", "julia"
    )  # mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
    # julia_cmd = mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
    if not os.path.exists(julia_cmd):
        print("Julia not present in path:", mpath, "...downloading...")
        subfolder = os.path.join(mpath, "tb3py", "julia")
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        # os.system("mkdir "+mpath+"/src/julia") # create a subfodler for julia
        os.chdir(subfolder)  # go to the subfolder
        # os.chdir(mpath+"/src/julia") # go to the subfolder
        ## download julia
        juliafile = os.path.join(
            mpath, "julia-1.6.1-linux-x86_64.tar.gz"
        )  # julia file
        # juliafile = os.path.join(mpath,"julia-1.6.1-linux-x86_64.tar.gz")  # julia file
        # j_link = "https://julialang-s3.julialang.org/bin/linux/x64/1.6/"
        j_link = (
            "https://julialang-s3.julialang.org/bin/linux/x64/1.6/"
            + "julia-1.6.1-linux-x86_64.tar.gz"
        )
        print("jlink", j_link)
        import requests
        import tarfile

        r_julia = requests.get(j_link, stream=True).content
        with open(juliafile, "wb") as jfile:
            jfile.write(r_julia)
        print("juliafile", juliafile)
        try:
            my_tar = tarfile.open(juliafile)
            my_tar.extractall()
            my_tar.close()
        except Exception as exp:
            print(exp)
            cmd = "tar -xvzf " + juliafile
            os.system(cmd)
        os.remove(juliafile)
        # os.system("wget https://julialang-s3.julialang.org/bin/linux/x64/1.6/"+juliafile)
        # os.system("tar -xvf "+juliafile) # untar the file
        # os.system("rm "+juliafile) # rm the file
    else:
        print("We already downloaded to ", julia_cmd)

    # julia_cmd = mpath+"/src/julia/julia-1.6.1/bin/julia" # path for julia
    os.chdir(mpath)  # go back

else:
    julia_cmd = "julia"
    print("Correct Julia version found in path")


print("My julia command : ", julia_cmd)

# install python dependences
# os.system("python3 -m pip install --user julia")

# using julia
# import julia
# julia.install()


# os.system("pip install pmdarima")


# install
sysimage = os.path.join(
    os.environ["HOME"], ".julia", "sysimages", "sys_threebodytb.so"
)
print("sysimage", sysimage)
if not os.path.isfile(sysimage):
    # import TB3.juliarun as juliarun
    install(julia_cmd)  # install Julia dependences

"""

from julia.api import Julia
jlsession = Julia(runtime=julia_cmd, compiled_modules=False, sysimage=sysimage)
jlsession.eval("using Suppressor") # suppress output

from julia import ThreeBodyTB
c = ThreeBodyTB.makecrys( [[5.0,0,0],[0,5.0,0],[0,0,5.0]] , [[0, 0, 0]], ["Li"])

print()
print("result of makecrys")
print(c)
print()
print("the end")
print()
"""
