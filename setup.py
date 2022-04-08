from distutils import extension
from ntpath import join
from setuptools import setup, Extension, find_packages
from distutils.sysconfig import get_python_lib
import os
import sys
import platform

VERSION = "19.0.3"

class BuildData():
    """
    BuildData()

    A class for holding data about Operating system
    and Lindo location/ version

    """
    def __init__(self):
        self.MAJOR = "19"
        self.MINOR = "0"
        self.LINGO_HOME = os.environ.get('LINGO_19_HOME')
        self.LINGO64_HOME = os.environ.get('LINGO64_19_HOME')
        self.platform = platform.system()
        self.is_64bits = sys.maxsize > 2**32

bd = BuildData()

try:
    import numpy
except Exception:
    print('\nWarning: numpy was not found, installing...\n')
    import subprocess
    subprocess.call([sys.executable, "-m", "pip", "install", "numpy"])

# include the numpy library
numpyinclude = os.path.join(get_python_lib(
      plat_specific=True), 'numpy/core/include/numpy')

# Gets the long description from README FILE
setupDir = os.path.dirname(__file__)
readmeFn = os.path.join(setupDir, "README.md")
with open(readmeFn, encoding="utf-8") as f:
    long_description = f.read()
    f.close()
    

if bd.platform == 'Windows':

    if bd.is_64bits:
        IncludePath = bd.LINGO64_HOME + '/Programming Samples'
        LibPath     = bd.LINGO64_HOME + '/Programming Samples' 
        LingoLib    = 'Lingd64_' + bd.MAJOR
    else:
        IncludePath = bd.LINGO_HOME + '/Programming Samples'
        LibPath = bd.LINGO_HOME + '/Programming Samples' 
        LingoLib = 'Lingd' + bd.MAJOR

    extra_link_args = '-Wl,--enable-stdcall-fixup'

if bd.platform == 'Linux':
    IncludePath = os.path.join(bd.LINGO64_HOME,'programming_samples')
    LingoLib = 'lingo64'
    LibPath = os.path.join(bd.LINGO64_HOME, 'bin/linux64')

    extra_link_args = '-Wl,-rpath-link,' + LibPath + ' -Wl,-rpath,' + LibPath
    macros = []


extension_kwargs = {
                    "name" : "lingo_api.lingo",
                    "sources" : ["src/lingo_api/pyLingo.c"],
                    "include_dirs" : [IncludePath, numpyinclude],
                    "library_dirs" : [LibPath],
                    "libraries" : [LingoLib],
                    "depends":[LibPath],
                    "extra_link_args" : [extra_link_args]
                    }


lingomodule = Extension(**extension_kwargs)

setup_kwargs = {"name" : 'lingo-api',
                "version" : VERSION,
                "description" : 'Python interface to LINGO API',
                "long_description": long_description,
                "author" : 'Zhe Liu',
                "author_email" : 'kevin@lindo.com',
                "url" : 'http://www.lindo.com',
                "classifiers": [
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3 :: Only",],
                "python_requires": ">=3.7",
                "platforms" : ['Windows, Linux'],
                "ext_modules" : [lingomodule],
                "install_requires": ["numpy>=1.19"],
                "package_dir": {"": "src"},
                "packages" : ['lingo_api', 'lingo_test'],
                "package_data" : {'lingo_api': ['*.txt', 'pyLingo.c']},}

setup(**setup_kwargs)
       

       
