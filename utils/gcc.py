from cargs import Project

def create_cmd(
	compiler:str,
	project) -> str:
	
	version  :str  = project.version.lower() if project.version else ""
	optimized :bool = True if project.optimize == "on" else False

	version_flag  :str  = f'-std={version}' if version != "" else ""
	
	cmd = f'{compiler} {version_flag}'

	for file in project.srcfiles:
		cmd += f' ./{file} '
		

	for folder in project.includedirs:
		cmd += f' -I{folder} '

	for folder in project.libdirs:
		cmd += f' -L{folder} '

	for warning in project.warnings:
		cmd += f' -W{warning} '
	
	for define in project.defines:
		cmd += f' -D{define} '

	for file in project.libfiles:
		cmd += f' -l{file} '
		
	cmd += (" -O3 " if optimized else "-O0 ")
	cmd += f'-o{project.executable_path()}'

	return cmd
