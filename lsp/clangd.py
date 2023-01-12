from pathlib import Path 
from project import Project

def create_config_file(project : Project) -> str:
    relative_includes = ['-I'+ str(Path(include)).replace('\\','/') for include in project.includedirs]
    directory = str(project.workingdir.resolve()).replace('\\','/')
    config_str = f"""
[
    {{
        "directory":"{directory}"
        "command" : "g++ {' '.join(relative_includes)}"
        "file": ""
    }}
]
"""
    return config_str
