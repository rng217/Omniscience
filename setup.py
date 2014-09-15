#setup.py build --compiler=mingw32

from distutils.core import setup, Extension

setup (name = '_omniscience',
       ext_modules = [Extension('_omniscience',sources = ['_omniscience.c'],extra_compile_args=['-std=gnu99','-Ofast'])])

import shutil
shutil.copy("./build/lib.win32-2.7/_omniscience.pyd",".")