import time
import psutil
import datetime
import pprint
from navalmartin_mir_db_utils.schemata import TaskPerformanceResultSchema, TaskResultSchema


def sum_task(sleep_time: int, n_elements: int):
    time.sleep(sleep_time)

    total = sum([i for i in range(n_elements)])
    return total


if __name__ == '__main__':
    start_time = time.time()

    pp = pprint.PrettyPrinter(indent=4)
    task_performance = TaskPerformanceResultSchema()
    task_result = TaskResultSchema()

    sum = sum_task(sleep_time=3,
                   n_elements=1000000)

    task_result.results = [{'sum': sum}]

    virtual_mem_dict = dict(psutil.virtual_memory()._asdict())
    cpu_percentage = psutil.cpu_percent()

    pp.pprint(f"Task virtual memory dictionary: {virtual_mem_dict}")
    pp.pprint(f"Task CPU performance: {cpu_percentage}")

    end_time = time.time()
    task_performance.latency = end_time - start_time
    task_performance.ended_at = datetime.datetime.utcnow()
    task_performance.cpu_util = cpu_percentage
    task_performance.disk_util = virtual_mem_dict

    pp.pprint(f"Task performance: {task_performance}")
    pp.pprint(f"Task result: {task_result}")
