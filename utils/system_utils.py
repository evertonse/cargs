import contextlib
import os


@contextlib.contextmanager
def pushd(new_dir):
  previous_dir = os.getcwd()
  os.chdir(new_dir)
  try:
      yield
  finally:
      os.chdir(previous_dir)
#You can then use it like the following:

import subprocess
def executable(exe:str):
  try:
    subprocess.call([exe, '--version'])
    return True
  except OSError:
    return False
