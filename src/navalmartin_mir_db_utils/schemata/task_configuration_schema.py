from pydantic import BaseModel, Field
from typing import Dict


class TaskConfigurationSchema(BaseModel):
    task_input: Dict = Field(title="task_input",
                                  description="The input for the task",
                                  default={})

    detail: Dict = Field(title="detail",
                               description="Details pertaining to the task",
                               default={})

    task_packages_versions_required: Dict = Field(title="task_packages_versions_required",
                                                  description="Specific packages versions the task requires",
                                                  default={})

    stage_task_id: int = Field(title="stage_task_id",
                               description="The id of the stage that this task has. "
                                           "By default it is assumed that the task is not part of any StagedTask",
                               default=-1)

    has_next_stage: bool = Field(title="has_next_stage",
                                 description="Flag indicating if the task has a next stage. "
                                             "By default it is assumed that the task is not part of any StagedTask",
                                 default=False)

    next_stage_id: int = Field(title="next_stage_id",
                               description="If the task has next stage then this is id of the next stage. "
                                           "By default it is assumed that the task is not part of any StagedTask",
                               default=-1)
