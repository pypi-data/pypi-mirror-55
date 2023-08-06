from pangeamt_tea.project.workflow.stage.abstract_stage import AbstractStage


class Clean(AbstractStage):
    NAME = 'clean'
    def __init__(self, workflow):
        super().__init__(workflow, self.NAME)

    def run(self):
        return {

        }