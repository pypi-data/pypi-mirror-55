import json
import time

from scrapper_core.config import CONFIG
from scrapper_core.exception import RetryTaskExitError, RetryTaskError, RetryTaskSkipAuthError
from scrapper_core.helper import retry_task, EnhancedJSONEncoder
from scrapper_core.types import ScrapperData, TaskData
from .blueprint_scrapper import BlueprintScrapper


class Scrapper:
    @staticmethod
    def _run_task(task: TaskData, scrapper_data: ScrapperData):
        package_name, classname = task.action.rsplit('.', 1)
        blueprint = getattr(__import__(package_name, fromlist=[package_name]), classname)(scrapper_data, task)
        blueprint.fetch()
        blueprint.transform()
        time.sleep(blueprint.interval())
        return blueprint.action_data

    @staticmethod
    @retry_task(times=CONFIG.get('RETRY_TASK_COUNT'))
    def _run(scrapper: BlueprintScrapper, is_auth=True):
        if is_auth:
            scrapper.authenticate()
        for task in [task for task in scrapper.data.tasks if task.action_data is None]:
            task.action_data = Scrapper._run_task(task, scrapper.data)

    @staticmethod
    def run(scrapper: BlueprintScrapper, json_output=True):
        try:
            Scrapper._run(scrapper)
            return json.dumps(scrapper.data, cls=EnhancedJSONEncoder) if json_output else scrapper.data
        except (RetryTaskExitError, RetryTaskError, RetryTaskSkipAuthError) as e:
            scrapper.data.is_valid = False
            scrapper.data.error_message = e.message
            scrapper.data.error_extra = e.extra
            return json.dumps(scrapper.data, cls=EnhancedJSONEncoder) if json_output else scrapper.data
