#setup.py build --compiler=mingw32

from distutils.core import setup, Extension

setup (name = 'omnisciencemodule',
       ext_modules = [Extension('omnisciencemodule',sources = ['omnisciencemodule.c'],extra_compile_args=['-std=gnu99','-Ofast'])])

import shutil
shutil.copy("./build/lib.win32-2.7/omnisciencemodule.pyd",".")