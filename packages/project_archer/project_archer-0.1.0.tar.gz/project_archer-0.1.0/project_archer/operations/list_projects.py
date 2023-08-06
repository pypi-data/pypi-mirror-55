import os

from project_archer.environment.read_shell_parameters import project_folder
from project_archer.storage.project_data import read_project_yml

def list_projects(args, env):
    folder = project_folder(args)

    env.log("Available projects:")

    for filename in os.listdir(folder):
        if not os.path.isfile(os.path.join(folder, filename)):
            continue

        file_data = open(os.path.join(folder, filename))
        project_data = read_project_yml(file_data)
        env.log(" - " + filename + ": " + project_data['name'])
