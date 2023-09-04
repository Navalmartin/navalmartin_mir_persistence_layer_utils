"""module task_performance_result_schema. Models basic schema
for monitoring the performance of a task. The schema is meant
to be embedded in a task document specified by the client code

"""

from pydantic import BaseModel, Field
from typing import List, Dict

from navalmartin_mir_db_utils.utils import InvalidTypeEnum


class ErrorType(BaseModel):
    label: str = Field(title="label",
                       description="Identifier for the error",
                       default=InvalidTypeEnum.INVALID.name.upper())
    error_description: str = Field(title="error_description",
                                   description="Textual description of the error",
                                   default=InvalidTypeEnum.INVALID.name.upper())
    details: dict = Field(title="details",
                          description="Details pertaining to the specific error",
                          default={})


class TaskResultSchema(BaseModel):
    errors: Dict = Field(title="errors",
                                    description="The errors occurred whilst the task was running",
                                    default={})
    results: Dict = Field(title="results",
                          description="The results obtained by running the task was running",
                          default={})
