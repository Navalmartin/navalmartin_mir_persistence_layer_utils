from typing import Any, List
import psutil
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import (CreateEntityCRUDAPI, UpdateEntityCRUDAPI)
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.utils.db_enums import TaskStateTypeEnum
from navalmartin_mir_db_utils.dbs.dbs_utils import is_valid_object_id


async def write_to_task_error_collection(event: dict,
                                         error_msg: str,
                                         task_id: str,
                                         error_type: str,
                                         lambda_arn: str,
                                         lambda_request_id: str,
                                         db_session: MongoDBSession,
                                         collection_name: str) -> Any:
    response = CreateEntityCRUDAPI.do_insert_one(data={"event": event,
                                                       'error_msg': error_msg,
                                                       'task_id': task_id,
                                                       "error_type": error_type,
                                                       "lambda_arn": lambda_arn,
                                                       "lambda_request_id": lambda_request_id},
                                                 db_session=db_session,
                                                 collection_name=collection_name)
    return response


async def finish_task(task_id: str,
                      result: dict,
                      total_time: float,
                      db_session: MongoDBSession,
                      collection_name: str) -> Any:
    oid = is_valid_object_id(oid=task_id)
    virtual_mem_dict = dict(psutil.virtual_memory()._asdict())
    cpu_percentage = psutil.cpu_percent()

    data = {'latency': total_time,
            'cpu_util': cpu_percentage,
            'disk_util': virtual_mem_dict,
            'gpu_util': 0.0,
            'cpu_mem_util': 0.0,
            'gpu_mem_util': 0.0,
            'errors': [],
            'task_state': TaskStateTypeEnum.FINISHED.name.upper(),
            'result': result
            }

    response = await UpdateEntityCRUDAPI.do_update_one(criteria={'_id': oid},
                                                       update_data=data,
                                                       db_session=db_session,
                                                       collection_name=collection_name)
    return response


async def finish_task_with_errors(task_id: str,
                                  errors: List[dict],
                                  total_time: float,
                                  db_session: MongoDBSession,
                                  collection_name: str) -> Any:
    """Finish the given task with errors

    Parameters
    ----------
    task_id: The task is
    errors: The errors list
    total_time: The total time the task lasted
    db_session: The MongoDB session
    collection_name: The collection name to write to

    Returns
    -------

    """
    oid = is_valid_object_id(oid=task_id)
    virtual_mem_dict = dict(psutil.virtual_memory()._asdict())
    cpu_percentage = psutil.cpu_percent()

    data = {'latency': total_time,
            'cpu_util': cpu_percentage,
            'disk_util': virtual_mem_dict,
            'gpu_util': 0.0,
            'cpu_mem_util': 0.0,
            'gpu_mem_util': 0.0,
            'errors': errors,
            'task_state': TaskStateTypeEnum.FINISHED.name.upper()
            }
    response = await UpdateEntityCRUDAPI.do_update_one(criteria={'_id': oid},
                                                       update_data=data,
                                                       db_session=db_session,
                                                       collection_name=collection_name)
    return response
