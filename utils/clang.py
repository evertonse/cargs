from cargs import Project

from pathlib import PurePath as Path


def create_cmd(compiler: str, project) -> str:

    version: str = project.version.lower() if project.version else ""
    optimized: bool = project.optimize  or 'off'
    debug: bool = project.debug or 'off' 

    version_flag: str = f"-std={version}" if version != "" else ""

    cmd = f"{compiler} {version_flag}"
    cmd += f"{' -fsanitize=address ' if debug else ''}"

    for file in project.srcfiles:
        cmd += f" {Path(file)} "

    for folder in project.includedirs:
        cmd += f" -I{Path(folder)} "

    for folder in project.libdirs:
        cmd += f" -L{Path(folder)} "

    for warning in project.warnings:
        cmd += f" -W{warning} "

    for define in project.defines:
        cmd += f" -D{define} "

    for file in project.libfiles:
        cmd += f" -l{file} "

    cmd += " -O3 " if optimized == 'on' else " -O0 "
    cmd += " -g " if debug == 'on' else " -g0 "
    cmd += f"-o{project.executable_path()}"

    return cmd
