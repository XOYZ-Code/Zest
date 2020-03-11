from modules.version_control import Project
from modules.system import File, System
from modules.style import Style


# Initialize Project Objects
project = Project('image_upscaler', 'XOYZ-Code [xoyz.productions@gmail.com]')
project.initialize_project_build()
statistics = project.Statistics()
statistics.update_stat('Project Version', project.project_version_str)
file = File()
system = System('data/system/config.dll')
style = Style()
project.log('Sucessfully initialized all needed Project objects')
