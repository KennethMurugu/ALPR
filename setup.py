# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)
from cx_Freeze import setup, Executable
includes=['scipy']
excludes=[]


options = {
    'build_exe': {
    	'packages':['scipy', 'pytesseract'],
        'include_files': ['resources/','C:\\Users\\Kenneth\\Anaconda2\\Lib\\site-packages\\scipy\\special\\_ufuncs.pyd'],
        'excludes': ['collections.abc']
    }
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('alpr.py', base=base)
]
s
options
setup(name='ALPR',
      version='0.1.1',
      description='ALPR',
      executables=executables,
      options=options
      )
