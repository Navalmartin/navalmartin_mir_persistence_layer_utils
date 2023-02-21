from typing import Any
from navalmartin_mir_db_utils.dbs.dbs_utils import DB_ERROR
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.utils.exceptions import (ResourceNotFoundException, ResourceNotUpdatedException)

async def get_one_result_or_raise(
    crud_handler,
    criteria: dict,
    db_session: MongoDBSession,
    projection: dict = {},
    error_message: str = "Error occurred"
):

    """Query the handler about a result and raise
    ResourceNotFoundException if the query does not return any
    result
    """
    result = await crud_handler.find_one(
        criteria=criteria, db_session=db_session, projection=projection
    )

    if result is None:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotFoundException()

    return result

async def update_one_or_raise(
    crud_handler: Any,
    criteria: dict,
    db_session,
    update_data: dict,
    error_message: str = "Error occurred",
):
    result = await crud_handler.update_one(
        criteria=criteria, db_session=db_session, update_data=update_data
    )

    if result is None:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))

    if result.modified_count != 1 :
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))

    return result