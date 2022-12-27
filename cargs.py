import sys
from dataclasses import dataclass
from pathlib import Path, PurePath
import os
import subprocess
import tomllib as toml
import argparse as argp
from collections import defaultdict


import utils.color as color
from utils.log import debug, set_project
#from utils.package_test import package_setup
from utils.file import content_of


from utils import gcc
from utils import msvc

__dir_path__ = os.path.dirname(os.path.realpath(__file__))
__filename__,_ =  __file__[__file__.rindex('\\')+1:].rsplit('.',1)

# >>========================================================================================================
# >>=============================================CONFIG PROEJCT=============================================
# WARNING:
# 	require either tomllib installed or python 3.11 (tomllib became part of the standard library for python 3.11)
# PLEASE:
# 	Create a toml files as your project config
# 	Define **ALL** variables listed in the class Project bellow, 
# 	Then populate with the desired values using the type indicated below
@dataclass
class Project():
  name: str 

  compiler: str		# can optionally use full path
  language: str  	# ignored for now
  version : str
  binpath : str # directory for binaries, if
  
  # -O
  optimize: str
  
  srcfiles 		: list[str]
  # -D
  defines 		: list[str]
  # -I
  includedirs	: list[str]
  # -L
  libdirs 		: list[str]
  # -l
  libfiles 		: list[str]
  # -W
  warnings 		: list[str]
#<<=========================================================================================================
#<<=========================================================================================================

  def __init__(self,toml_dict) -> None:
    self.__dict__ = toml_dict
    self.binpath = Path(PurePath('./'+ toml_dict['binpath']))
    self.binpath.mkdir(parents=True,exist_ok=True)
    self.add_src_files()

  # // TODO(Everton): "ADD Regex to this"
  def add_src_files(self):
    for srcfile in list(self.srcfiles):
      if srcfile.endswith("**"):
        
        srcdir = srcfile[:len(srcfile)-2]
        for file in os.listdir(srcdir):
          if file.endswith(".cpp") or file.endswith(".c"):
            self.srcfiles.append(os.path.join(srcdir, file))
        
        self.srcfiles.remove(srcfile)

  def executable_path(self):
    return str(PurePath(self.binpath,self.name))

# cdir = os.getcwd() # it will return current working directory
# print("Previous_dir",cdir)

# # Previous_dir C:\Users\..\Desktop\python
# os.chdir('./..') #chdir used for change direcotry
# print("Current_dir",cdir)


def create_cmd(
  compiler:str,
  project:Project) -> str:
  if compiler.lower() in {'msvc', 'cl'}:
    debug(f"INFO: detected msvc build")
    return msvc.create_cmd('cl',project)
  else:
    debug(f"INFO: detected gcc build")
    return gcc.create_cmd('g++',project)

def create_empty_build(path):
  build_default_name = "build.toml"
  
  filepath = Path(path,build_default_name)
  debug(f"INFO: about to create default build file {filepath}")
  default_filepath = Path(__dir_path__+'/assets/default.toml')
  
  if not os.path.exists(filepath):
    debug(f"INFO: about to read default build from {default_filepath}")
    with open(filepath, 'w') as f:
      f.write(content_of(default_filepath))
      debug(f"INFO: {build_default_name} was added as the build file")
  else: 
    debug(f"INFO: {build_default_name} already exists, nothing was done.")

def process_commands():
  if len(sys.argv) > 1:
    if sys.argv[1].lower() in {'init','start'} :
      create_empty_build('')
      exit(0)

def __main__():
  set_project(name=__filename__) # setting up dependencies

  project_path = sys.argv[1] if len(sys.argv) > 1 else exit(debug("Error: Where toml at?"))
  debug(f"INFO: about to process args")
  process_commands()

  with open(project_path, "rb") as f:
    data	 	= defaultdict(lambda:"",toml.load(f))
    project = Project(data)
  
  config = {
    "compiler" : project.compiler if project is not None else 'g++', 
  }
  cmd = create_cmd(
    compiler=config['compiler'],
    project =project
  )
  
  debug(f"INFO: Building project from file : {color.BLUE(project_path)}")
  debug(f"INFO: Command Generated: {cmd}")
  debug(f"INFO: Running project from file : {color.BLUE(project_path)}")
  
  code = subprocess.run(cmd)
  
  if code.returncode == 0:
    debug(f'INFO: {color.GREEN("Compilation Succeded")} return code was zero, usually means success')
    subprocess.run(project.executable_path())
  else:
    debug(f'ERROR: {color.RED("Compilation Failed")} return code was {color.RED("non-zero")}, usually means bad things')

if __name__ == '__main__':
  __main__()
