from typing import List, Any, Text


def load_from_static_data(data: List[Any], **kwargs) -> List[Any]:
    return data


def load_from_mysql(sql: Text, **kwargs) -> List[Any]:
    # TODO Implementation required
    pass


def load_from_redshift(sql: Text, **kwargs) -> List[Any]:
    # TODO Implementation required
    pass

