"""module task_performance_result_schema. Models basic schema
for monitoring the performance of a task. The schema is meant
to be embedded in a task document specified by the client code

"""

from pydantic import BaseModel, Field


class TaskPerformanceResultSchema(BaseModel):

    latency: float = Field(title='latency',
                           description="The overall time the task lasted",
                           default=0.0)
    disk_util: dict = Field(title='disk_util',
                            description="The disk utilization of the task",
                            default={})
    cpu_util: float = Field(title='cpu_util',
                            description="The percentage of the CPU utilization",
                            default=0.0)
    gpu_util: float = Field(title='gpu_util',
                            description="The percentage of the GPU utilization",
                            default=0.0)
    cpu_mem_util: float = Field(title='cpu_mem_util',
                                description="The percentage of the CPU-RAM utilization",
                                default=0.0)
    gpu_mem_util: float = Field(title='gpu_mem_util',
                                description="The percentage of the GPU-RAM utilization",
                                default=0.0)