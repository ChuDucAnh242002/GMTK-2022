from cx_Freeze import Executable, setup
import sys

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable("main.py", base=base),
]

setup(
    name= "platformer",
    version= "0.1",
    description = "cx_Freeze script",
    options = {'build_exe': {"packages": ["pygame", "sys", "player", "game", "color", "core_funcs", "text", "animation", "entity", "tilemap"], "include_files": ["assets/", "help.txt"]}},
    executables = executables
)