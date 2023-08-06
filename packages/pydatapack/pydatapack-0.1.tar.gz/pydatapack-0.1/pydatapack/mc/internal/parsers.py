import enum
import json
from types import FunctionType, MethodType

from pydatapack import utils

__all__ = ['json_parser', 'default_parser']


def json_parser(arg) -> str:
    return json.dumps(arg)


def default_parser(arg) -> str:
    if isinstance(arg, enum.Enum):
        return utils.pascal_to_snake_case(arg.name).strip('_').replace('_', '-')

    elif isinstance(arg, bool):
        return str(arg).lower()

    # If class
    elif isinstance(arg, type):
        return utils.pascal_to_snake_case(arg.__name__).strip('_').replace('_', '-')

    # If function
    elif isinstance(arg, (FunctionType, MethodType)):
        return arg.__name__.strip('_').replace('_', '-')

    else:
        return str(arg)
