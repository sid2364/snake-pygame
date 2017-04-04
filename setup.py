import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["time", "pygame", "math"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "snake",
        version = "0.1",
        keywords = "snake",
        license = "Python Software Foundation License",
        maintainer = "Siddharth Sahay",
        maintainer_email = "sahaysid@gmail.com",
        description = "Snake!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("snake.py", base=base)])

