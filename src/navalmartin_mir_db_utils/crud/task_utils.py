from typing import Any, List
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import CreateEntityCRUDAPI
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession


async def write_to_task_error_collection(event: dict,
                                         error_msg: str,
                                         task_id: str,
                                         error_type: str,
                                         lambda_arn: str,
                                         lambda_request_id: str,
                                         db_session: MongoDBSession,
                                         collection_name: str) -> Any:
    response = await CreateEntityCRUDAPI.insert_one(data={"event": event,
                                                          "task_id": task_id,
                                                          'error_msg': error_msg,
                                                          "error_type": error_type,
                                                          "lambda_arn": lambda_arn,
                                                          "lambda_request_id": lambda_request_id},
                                                    db_session=db_session,
                                                    collection_name=collection_name)
    return response
