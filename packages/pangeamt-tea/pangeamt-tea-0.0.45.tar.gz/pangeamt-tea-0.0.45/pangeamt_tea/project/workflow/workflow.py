import os


class Workflow:
    DIR = 'workflow'

    def __init__(self, project, config):
        self._project = project
        self._config = config

    @staticmethod
    def new(project, force=False):
        pass
        # if force=True remove remove the workflow first
        # Create the worflow dir if the directory doesn't exists else raise WorkflowAlreadyExists
        # Create the config.json threw the project.worflow.config

    @staticmethod
    def load(project):
        pass
        # Return a Workflow

    @staticmethod
    def remove(project):
        pass
        # Remove the worflow dir




class WorkflowAlreadyExists(Exception):
    def __init__(self, project):

        message = f'The workflow already exists in project {project.name} '
        super().__init__(message)