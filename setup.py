from cx_Freeze import setup, Executable

executables = [Executable(script="main.py", base="Win32GUI")]
buildOptions = dict(includes=["animator", "map", "player"], include_files=['src/'])

setup(
    name="Resistance - Jeu 1",
    version="1",
    description="Premier mini-jeu du projet d'histoire",
    author="Marc-Aurèle",
    options=dict(build_exe=buildOptions),
    executables=executables
)