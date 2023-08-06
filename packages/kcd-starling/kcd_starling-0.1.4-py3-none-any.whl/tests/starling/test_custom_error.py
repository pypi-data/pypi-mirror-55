from starling.app import Scrapper
from starling.blueprint_action import BlueprintAction
from starling.blueprint_scrapper import BlueprintScrapper
from starling.config import CONFIG
from starling.exception import RetryTaskExitError, RetryTaskSkipAuthError
from starling.types import ScrapperData


class MyRetryTaskExitErrorScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_custom_error.MyActionWithRetryTaskExitError1',
            'tests.starling.test_custom_error.MyActionWithRetryTaskExitError2'
        ]

    def authenticate(self):
        pass


class MyActionWithRetryTaskExitError1(BlueprintAction):
    def fetch(self):
        self.action_data.fetched_data = self.action_data.fetched_data if self.action_data is None else 0 + 1

    def transform(self):
        raise RetryTaskExitError('ip blocked')


class MyActionWithRetryTaskExitError2(BlueprintAction):
    def fetch(self):
        self.action_data.fetched_data = self.action_data.fetched_data if self.action_data is None else 0 + 1

    def transform(self):
        raise RetryTaskExitError('ip blocked')


class MyRetryTaskSkipAuthErrorScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_custom_error.MyActionWithRetryTaskSkipAuthError1',
            'tests.starling.test_custom_error.MyActionWithRetryTaskSkipAuthError2'
        ]

    def authenticate(self):
        pass


retry_task_skip_auth_error_counter = 0


class MyActionWithRetryTaskSkipAuthError1(BlueprintAction):
    def fetch(self):
        self.action_data.fetched_data = 1

    def transform(self):
        self.action_data.transformed_data = self.action_data.fetched_data


class MyActionWithRetryTaskSkipAuthError2(BlueprintAction):
    def fetch(self):
        self.action_data.fetched_data = 2

    def transform(self):
        global retry_task_skip_auth_error_counter
        retry_task_skip_auth_error_counter += 1
        raise RetryTaskSkipAuthError('retry task but skip auth', extra={'id': '12345'})


def test_scrapper_with_retry_task_exit_error():
    res = Scrapper.run(MyRetryTaskExitErrorScrapper(ScrapperData('place', {'place_id': '123123'}))
                       , json_output=False)

    assert "ip blocked" == res.error_message
    assert res.tasks[0].action_data is None
    assert res.tasks[1].action_data is None
    assert res.is_valid is False


def test_scrapper_with_retry_task_skip_auth_error():
    res = Scrapper.run(MyRetryTaskSkipAuthErrorScrapper(ScrapperData('place', {'place_id': '123123'}))
                       , json_output=False, task_retry_times=5)
    global retry_task_skip_auth_error_counter
    assert "retry task but skip auth" == res.error_message
    assert res.error_extra['id'] == '12345'
    assert res.tasks[0].action_data.fetched_data == 1
    assert res.tasks[1].action_data is None
    assert res.is_valid is False
    # TODO should search another better ways that check retry count properly
    assert retry_task_skip_auth_error_counter == CONFIG.get('task_retry_times')
    assert retry_task_skip_auth_error_counter == 5
