import abc
from scrapper_core.bucket import Bucket


class Blueprint(abc.ABC):
    def __init__(self, topic, candidates=None):
        self.topic = topic
        self.candidates = candidates

    @abc.abstractmethod
    def loader(self):
        raise NotImplementedError('loader function should be written')

    @abc.abstractmethod
    def get_credential(self, candidate):
        raise NotImplementedError('loader function should be written')

    @abc.abstractmethod
    def fetch(self, candidate, credential):
        raise NotImplementedError('fetch function should be written')

    @abc.abstractmethod
    def transform(self, candidate, data):
        raise NotImplementedError('transform function should be written')

    @property
    def buckets(self):
        return [Bucket.Stdout]

    @abc.abstractmethod
    def fetch_sleep(self, data):
        return 0
