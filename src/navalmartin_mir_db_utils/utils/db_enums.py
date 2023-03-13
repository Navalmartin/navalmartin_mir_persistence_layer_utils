"""module db_enums. Various useful enumerations

"""
from enum import Enum


class InvalidTypeEnum(Enum):
    INVALID = 0


class TaskStateTypeEnum(Enum):
    INVALID = 0
    CANCELLED = 1
    IN_PROGRESS = 2
    PENDING = 3
    FINISHED = 4
    FINISHED_WITH_ERRORS = 5


class ErrorTypeEnum(Enum):
    UNKNOWN_ERROR = 0
    GENERAL_SQS_MESSAGE_ERROR = 1
    GENERAL_DATA_ERROR = 2
    FRAMEWORK_EXCEPTION = 3
    INCORRECT_RESULT = 4
