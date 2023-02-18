from dataclasses import dataclass
from pathlib import Path, PurePath
from glob import glob
import os
import tomllib as toml

from collections import defaultdict

#from utils.package_test import package_setup

# @dataclass


class Project():
    name: str

    compiler: str		# can optionally use full path
    language: str  	# ignored for now
    version: str
    binpath: str  # directory for binaries, if

    workingdir: Path  # workingdir

    # -O
    optimize: str

    srcfiles: list[str]
    # -D
    defines: list[str]
    # -I
    includedirs: list[str]
    # -L
    libdirs: list[str]
    # -l
    libfiles: list[str]
    # -W
    warnings: list[str]

# <<=========================================================================================================
# <<=========================================================================================================
    def __init__(self, toml_dict, abs_path=False) -> None:
        self.__dict__ = toml_dict
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
        print(project_path)
        with open(str(project_path), "rb") as f:
            data = defaultdict(lambda: "", toml.load(f))
            project = cls(data, abs_path)
        return project

    @classmethod
    def from_dict(cls, obj_dict: dict, abs_path=False):
        project = cls(obj_dict, abs_path)
        return project

    # // TODO(Everton): "ADD Regex to this"
    # // TODO(Everton): "ADD Regex to this"
    def add_src_files(self):
        for srcfile in list([str(f) for f in self.srcfiles]):
            if srcfile.endswith("*"):

                srcdir = srcfile[:len(srcfile)-2]
                for file in os.listdir(srcdir):
                    if file.endswith(".cpp") or file.endswith(".c"):
                        self.srcfiles.append(Path(srcdir, file))

                self.srcfiles.remove(srcfile)

    def add_include_dirs(self):
        resolved_includedirs = []
        for dir in self.includedirs:
            for resolved_dir in glob(dir + '/' if not dir.endswith('/') else dir, recursive=True):
                resolved_includedirs.append(Path(resolved_dir))
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
