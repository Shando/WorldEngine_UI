from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=["PyQt4", "gdal", "numpy", "os", "osgeo", "email.mime", "array", "audioop", "binascii", "cPickle", "cStringIO", "cmath", "datetime", "email", "errno", "exceptions", "future_builtins", "gc", "hashlib", "imageop", "imp", "itertools", "marshal", "math", "mmap", "msvcrt", "nt", "operator", "parser", "protobuf", "signal", "socket", "strop", "sys", "thread", "time", "xxsubtype", "zipimport", "zlib"], excludes=[], include_files = [])

import sys
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('setup.py', base=base, targetName='worldengine_gui.exe')
]

setup(name='WorldEngine_GUI',
      version='0.1',
      description='GUI for WorldEngine',
      options=dict(build_exe=buildOptions),
      executables=executables)
