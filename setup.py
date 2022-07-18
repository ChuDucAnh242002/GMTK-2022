from cx_Freeze import Executable, setup
import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable("BoBoiGirl.py", base=base),
]

setup(
    name= "BoBoiGirl",
    version= "0.1",
    description = "cx_Freeze script",
    options = {
        'build_exe': {"packages": ["random", "pygame"], 
        "include_files": ["data/", "engine/", "mechanic/"]
        }
    },
    executables = executables
)