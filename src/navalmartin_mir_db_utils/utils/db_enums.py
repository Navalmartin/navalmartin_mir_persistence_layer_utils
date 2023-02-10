"""module db_enums. Various useful enumerations

"""
from enum import Enum


class TaskStateTypeEnum(Enum):
    INVALID = 0
    CANCELLED = 1
    IN_PROGRESS = 2
    PENDING = 3
    FINISHED = 4


class ErrorTypeEnum(Enum):
    UNKNOWN_ERROR = 0
    GENERAL_SQS_MESSAGE_ERROR = 1
    GENERAL_DATA_ERROR = 2