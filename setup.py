#!/usr/bin/python3
import os
import sys
import subprocess

# import requests
import glob
import os

from setuptools import setup, find_packages


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
    print("precompile done")


def install(julia=None):
    """Install Julia and TB"""
    if julia is None:
        julia = "julia"  # julia command
    print("install ", julia)
    # NOTE: For a new Github release:
    # rm ~/.julia/sysimages/sys_threebodytb.so
    os.system(
        julia
        + " --eval "
        + '"import Pkg; Pkg.add(url=\\"https://github.com/usnistgov/ThreeBodyTB.jl\\")"'
    )
    # os.system(julia + " --eval " + '"import Pkg; Pkg.add(ThreeBodyTB")"')
    # os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"ThreeBodyTB\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"PyCall\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"Plots\\")"')
    os.system(julia + " --eval " + '"import Pkg; Pkg.add(\\"Suppressor\\")"')
    precompile(julia)


setup(
    name="tb3py",
    version="2021.11.11",
    long_description=long_d,
    install_requires=[
        "requests>=2.26.0",
        "numpy>=1.19.5",
        "julia>=0.5.6",
        "jarvis-tools",
        "cython",
        "pytest",
    ],
    extras_require={
        "jarvis-tools": ["jarvis-tools"],
        "julia": ["julia"],
    },
    author="Kevin Garrity, Kamal Choudhary",
    author_email="kevin.garrity@nist.gov",
    description=(
        "tb3: an open-source software package for accurate and efficient electronic structure calculations using tight-binding (TB), including three-body interactions. https://pages.nist.gov/ThreeBodyTB.jl"
    ),
    license="NIST",
    url="https://github.com/usnistgov/tb3py",
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
    raise ValueError("conda install -c conda-forge julia")
else:
    julia_cmd = "julia"
    print("Correct Julia version found in path")


sysimage = os.path.join(
    os.environ["HOME"], ".julia", "sysimages", "sys_threebodytb.so"
)
print("sysimage", sysimage)
if not os.path.isfile(sysimage):
    try:
        install(julia_cmd)  # install Julia dependences
    except Exception as exp:
        print(exp)
        pass
