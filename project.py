from dataclasses import dataclass
from pathlib import Path, PurePath
from glob import glob
from utils.log import debug
import os
try:
    import tomllib as toml
    tomllib_available = True 
except:
    tomllib_available = False
    
from collections import defaultdict

#from utils.package_test import package_setup

# @dataclass


class Project():
    name: str = 'default_name'

    compiler: str = 'gcc'		# can optionally use full path
    language: str = 'cpp'  	# ignored for now
    version: str = 'c+17'
    binpath: str  # directory for binaries, if

    workingdir: Path = Path('./')  # workingdir

    # -O
    optimize: str = 'off'

    # -g
    debug: str = 'off'

    srcfiles: list
    # -D
    defines: list
    # -I
    includedirs: list
    # -L
    libdirs: list
    # -l
    libfiles: list
    # -W
    warnings: list

# <<=========================================================================================================
# <<=========================================================================================================
    def __init__(self, toml_dict, abs_path=False) -> None:
        self.__dict__ = toml_dict
        print(f"project src files => {self.srcfiles}")
        self.binpath = Path(PurePath('./' + toml_dict['binpath']))
        self.binpath.mkdir(parents=True, exist_ok=True)
        # resolving paths, wild cards
        self.add_src_files()
        self.add_include_dirs()

        self.use_abs = False

        def create_path(f): return f'{Path(f)}'
        self.workingdir = Path(os.getcwd()).resolve() if not hasattr(
            self, 'workingdir') else Path(self.workingdir)
        if abs_path == True:
            def create_path(f): return f'"{Path(f).resolve()}"'
            self.use_abs = True

        self.srcfiles = [create_path(f) for f in self.srcfiles]
        self.includedirs = [create_path(f) for f in self.includedirs]
        self.libdirs = [create_path(f) for f in self.libdirs]
        #self.libfiles    = [Path(f).resolve() for f in self.libfiles]

    @classmethod
    def from_path(cls, project_path, abs_path=False) -> None:
        debug(project_path)
        with open(str(project_path), "rb") as f:
            if tomllib_available:
                data = defaultdict(lambda: "", toml.load(f))
            else:
                cmds = [
                    "python -m pip install --upgrade pip",
                    "python3 -m pip install --upgrade pip",
                    "python -m pip install --upgrade python",
                    "python3 -m pip install --upgrade python",
                ]

                debug("tomllib is not available, sorry you can ge1t it by upgranding to python 3.11")
                debug(" or 'pip install tomllib'")
                exit(1)
            project = cls(data, abs_path)
        return project

    @classmethod
    def from_dict(cls, obj_dict: dict, abs_path=False):
        project = cls(obj_dict, abs_path)
        return project

    # // TODO(Everton): "ADD Regex to this"
    # // TODO(Everton): "ADD Regex to this"
    def add_src_files(self):
        resolved_srcfiles = list()
        for srcfile in self.srcfiles.copy():
            print(f"project src files => {srcfile}")
            for resolved_file in glob(srcfile, recursive=True):
                resolved_file = Path(resolved_file) 
                if not resolved_file.is_dir():
                    resolved_srcfiles.append(Path(resolved_file))
        self.srcfiles = resolved_srcfiles

    def add_include_dirs(self):
        resolved_includedirs = []
        for dir in self.includedirs:
            for resolved_dir in glob(dir + '/' if not dir.endswith('/') else dir, recursive=True):
                resolved_dir = Path(resolved_dir) 
                if resolved_dir.is_dir():
                    resolved_includedirs.append(resolved_dir)
        self.includedirs = resolved_includedirs

    def executable_path(self):
        if self.use_abs:
            return '"' + str(Path(self.binpath, self.name).resolve()) + '"'
        return str(Path(self.binpath, self.name))

# cdir = os.getcwd() # it will return current working directory
# print("Previous_dir",cdir)

# # Previous_dir C:\Users\..\Desktop\python
# os.chdir('./..') #chdir used for change direcotry
# print("Current_dir",cdir)
