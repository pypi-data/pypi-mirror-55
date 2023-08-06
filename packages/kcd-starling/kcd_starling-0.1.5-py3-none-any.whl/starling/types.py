import typing
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class ScrapperData:
    topic: str
    candidate: typing.Any
    tasks: typing.List['TaskData'] = field(default_factory=list)
    auth_session: typing.Any = None
    error_message: str = None
    error_extra: dict = None
    is_valid: bool = True
    extra_config: dict = None


@dataclass
class TaskData:
    action: str
    action_data: 'ActionData' = None
    criteria: typing.Dict = field(default_factory=dict)


@dataclass
class ActionData:
    fetched_data: typing.Any = None
    transformed_data: typing.Any = None
