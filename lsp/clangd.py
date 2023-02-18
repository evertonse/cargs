from pathlib import Path 
from project import Project

def create_config_file(project : Project) -> str:
    relative_includes = ['-I'+ '\\"' + str(Path(include)).replace('\\','/') + '\\"' for include in project.includedirs]
    defines   = ['-D' + str(d) for d in project.defines]
    directory = str(project.workingdir.resolve()).replace('\\','/')
    config_str = f"""
[
    {{
        "directory":"{directory}",
        "command" : "{project.compiler}  {' '.join(defines)} {' '.join(relative_includes)}",
        "file": ""
    }}
]
"""
    return config_str
