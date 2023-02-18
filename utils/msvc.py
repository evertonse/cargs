from project import Project

from pathlib import PurePath as Path
def create_cmd(
	compiler:str,
	project) -> str:
	
	version  :str  = project.version.lower() if project.version else ""
	optimized :bool = True if project.optimize == "on" else False

	
	version_flag  :str  = f'-std:{version}' if version != "" else ""
	common_flags ="-"+" -".join(['MTd ' if not optimized else 'MT ','nologo '])

	cmd = f'{compiler} {version_flag} {common_flags}'
	cmd += f' -Fe:{project.executable_path()} '
  
  #/ZI option is similar to /Zi, but it produces a PDB file in a format that supports the Edit and Continue feature. 
  #/Z7 option produces object files that also contain full symbolic debugging information for use with the debugger.
	cmd += " -O2 " if optimized else " -Od -Zi "

	
	for define in project.defines:
		cmd += f' -D{define} '
	for warning in project.warnings:
		cmd += f' -W{warning} '

	for folder in project.includedirs:
		cmd += f' -I{Path(folder)} '
	#cmd += f'-Fo:{project.executable_path()}'

	for file in project.srcfiles:
		cmd += f' {Path(file)} '
		
	for file in project.libfiles:
		cmd += f' {file}.lib '

	cmd += f' -link '

	for folder in project.libdirs:
		cmd += f' -LIBPATH:{Path(folder)} '

	return cmd
