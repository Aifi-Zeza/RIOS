from cx_Freeze import setup, Executable
import os

# Определяем путь к папке assets
assets_folder = 'files/'

# Включаем всю папку assets
include_files = [
    (assets_folder, 'files'),  # Указываем путь к папке и как она будет называться в скомпилированной версии
]

build_exe_options = {
    "packages": ["tkinter","ast","PIL","marshal","vosk","sounddevice",],
    "include_files": include_files,
}

setup(
    name="RIOS",
    version="0.0.3",
    description="Alpha.",
    options={"build_exe": build_exe_options},
    executables=[Executable("src/main.py", base="Console")],
)