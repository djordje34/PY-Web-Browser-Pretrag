import os
import sys  # Imports are automatically detected (normally) in the script to freeze

import cx_Freeze

base = None 
from cx_Freeze import Executable, setup

if sys.platform=='win32':
    base = "Win32GUI"
#icon='icona.png'

#executables = [cx_Freeze.Executable("olg.py"),icon]    

target = Executable(
    script="pretrag.py",
    base="Win32GUI",
    #compress=False,
    #copyDependentFiles=True,
    #appendScriptToExe=True,
    #appendScriptToLibrary=False,
    icon="pretrag.ico"
)
"""
import os
import sys

import qdarktheme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
"""
cx_Freeze.setup(
        name = "Претраг the Browser",
        options = {"build_exe":{"packages":["os","sys","qdarktheme","PyQt5","psutil","time"],"include_files":["icons/","anim/"]}},
        version="1.0",
        executables=[target]) 
