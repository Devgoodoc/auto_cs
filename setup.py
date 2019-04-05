from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Goodoc\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Goodoc\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

build_exe_options = dict(
        packages = ["idna"],
        includes = ["sys", "os", "datetime", "tkinter", "slackclient", "gspread", "oauth2client", "urllib3", "json", "requests", "re", "threading", "logging"],
        include_files = ["cred.json", "tcl86t.dll", "tk86t.dll", "token_info.txt"]
)

#base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(
    name = "auto cs",
    version = "1.0",
    author="dave",
    description = "auto cs",
    options = {"build_exe": build_exe_options},
    executables = [Executable("auto_cs_1.py", base = "Win32GUI")]
)