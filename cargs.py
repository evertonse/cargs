#!/usr/bin/python3
import sys
import os
from pathlib import Path

from utils.log import debug, set_project

# from utils.package_test import package_setup
from utils.file import content_of
from utils.system_utils import pushd, executable

from utils import color
from compiler import msvc, clang, gcc

from lsp import clangd

from project import Project
import subprocess

__dir_path__ = os.path.dirname(os.path.realpath(__file__))
__filename__ = os.path.basename(__file__)

# >>========================================================================================================
# >>=============================================CONFIG PROEJCT=============================================
# WARNING:
# 	require either tomllib installed or python 3.11 (tomllib became part of the standard library for python 3.11)
# PLEASE:
# 	Create a toml files as your project config
# 	Define **ALL** variables listed in the class Project bellow,
# 	Then populate with the desired values using the type indicated below
# cdir = os.getcwd() # it will return current working directory
# print("Previous_dir",cdir)

# # Previous_dir C:\Users\..\Desktop\python
# os.chdir('./..') #chdir used for change direcotry
# print("Current_dir",cdir)


def create_cmd(compiler: str, project: Project) -> str:
    if compiler.lower() in {"msvc", "cl"}:
        debug(f"INFO: detected msvc build")
        return msvc.create_cmd("cl", project)

    elif compiler.lower() in {"clang", "clang++"}:
        debug(f"INFO: detected clang build")
        return clang.create_cmd(project.compiler, project)
    else:
        debug(f"INFO: detected gcc build")
        return gcc.create_cmd("g++", project)


def create_empty_build(path):
    build_default_name = "build.toml"

    filepath = Path(path, build_default_name)
    debug(f"INFO: about to create default build file {filepath}")
    default_filepath = Path(__dir_path__ + "/assets/default.toml")

    if not os.path.exists(filepath):
        debug(f"INFO: about to read default build from {default_filepath}")
        with open(filepath, "w") as f:
            f.write(content_of(default_filepath))
            debug(f"INFO: {build_default_name} was added as the build file")
    else:
        debug(f"INFO: {build_default_name} already exists, nothing was done.")


def process_help():
    cargs_help = {
        "init | start": "create an default build.toml file",
        "-h  | --help": "show help :P",
        "-d  | --debug ": "show debug information",
        "--clangd ": "generate clangd lsp config file (compile_commands.json)",
    }

    debug(
        f"\nC/C++ (C)ompiler (Args) automation with cargs.py\n"
        + f"Usage: cargs.py [ <options> ] <toml file>\n"
        + f"Options:\n  "
        + "\n  ".join([s[0].ljust(25) + s[1] for s in cargs_help.items()])
    )


def process_commands():
    if len(sys.argv) == 1:
        exit(debug("Error: Where .toml at? Use cargs init"))

    elif len(sys.argv) > 1:
        if sys.argv[1].lower() in {"init", "start"}:
            create_empty_build("")

        elif sys.argv[1].lower() in {"-h", "--help"}:
            process_help()

        elif sys.argv[1].lower() in {"--debug", "-d"}:
            debug("Args below:")
            for i, arg in enumerate(sys.argv):
                print(f"{i:>5}th arg: {arg}")

        elif sys.argv[1].lower() in {"--clangd"}:
            project = Project.from_path(sys.argv[2], abs_path=False)
            compile_commands: str = clangd.create_config_file(project)
            compiler_commands_path: str = Path(
                project.workingdir, "compile_commands.json"
            )
            with open(compiler_commands_path, "w+") as config_file:
                config_file.write(compile_commands)
            debug(
                f"DEBUG: Compiler Info for clangd create at {compiler_commands_path}")

        elif sys.argv[1].lower() in {"--autorun"}:
            debug(f"INFO: processing project files and auto running after build")
            process_build_file(sys.argv[2],autorun=True)

        else:
            debug(f"INFO: processing project files")
            process_build_file(sys.argv[1])
    else:
        exit(debug("Error: cargs doesn't support > 2 args right now ! sorry."))


def process_build_file(project_path: str, autorun=False):
    project = Project.from_path(project_path, abs_path=True)
    

    config = {
        "compiler": project.compiler if project is not None else "g++",
    }

    debug(f"INFO: Current Working Directory :  {color.BLUE(os.getcwd())}")
    cmd = create_cmd(compiler=config["compiler"], project=project)

    debug(f"INFO: Buioding project from file : {color.BLUE(project_path)}")
    debug(f"INFO: Command Generated: {cmd}")

    compiler_executale, _ = cmd.split(" ", 1)
    if not executable(compiler_executale):
        debug(
            f"ERROR: {color.RED(compiler_executale)} ain't no executable. Maybe it's not in the PATH?"
        )
        exit(1)
    with pushd(project.binpath):
        code = subprocess.run(cmd)

    if code.returncode == 0:
        debug(
            f'INFO: {color.GREEN("Compilation Succeded")} return code was zero, usually means success'
        )
        if autorun:
            debug(f"INFO: Running {color.BLUE(project.executable_path())}")
            os.startfile(project.executable_path())
            # subprocess.run(project.executable_path())
    else:
        debug(
            f'ERROR: {color.RED("Compilation Failed")} return code was {color.RED("non-zero")}, usually means bad things'
        )


def __main__():
    set_project(name=__filename__)  # setting up dependencies
    debug(f"INFO: about to process args")
    process_commands()


scary_global = 2
if __name__ == "__main__":
    __main__()
