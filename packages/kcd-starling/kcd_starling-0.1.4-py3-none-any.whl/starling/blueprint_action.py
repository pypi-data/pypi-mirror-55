import abc

from starling.types import ActionData, TaskData, ScrapperData


class BlueprintAction(abc.ABC):
    def __init__(self, scrapper_data: ScrapperData, task_data: TaskData):
        self.scrapper_data: 'ScrapperData' = scrapper_data
        self.task_data: 'TaskData' = task_data
        self.action_data: 'ActionData' = ActionData()

    @abc.abstractmethod
    def fetch(self):
        pass

    @abc.abstractmethod
    def transform(self):
        pass

    def interval(self) -> int:
        return 0
