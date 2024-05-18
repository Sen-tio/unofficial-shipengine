from enum import Enum


def serializer(inst, field, value):
    if isinstance(value, Enum):
        return value.value
    return value
