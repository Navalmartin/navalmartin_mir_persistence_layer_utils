from typing import Any
from navalmartin_mir_db_utils.dbs.dbs_utils import DB_ERROR
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import ReadEntityCRUDAPI
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.utils.exceptions import (ResourceNotFoundException, ResourceNotUpdatedException, ResourceExistsException)


async def get_one_result_or_raise(
        crud_handler: ReadEntityCRUDAPI,
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
        criteria=criteria, db_session=db_session, projection=projection,
        collection_name=crud_handler.collection_name
    )

    if result is None:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotFoundException(search_criteria=str(criteria))

    return result


async def if_resource_found_raise(crud_handler,
                                  criteria: dict,
                                  db_session: MongoDBSession,
                                  error_message: str = "Error occurred"):

    result = await crud_handler.find_one(
        criteria=criteria, db_session=db_session, projection={'_id': 1},
        collection_name=crud_handler.collection_name
    )

    if result is not None:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceExistsException(resource_id=str(criteria))


async def update_one_or_raise(
        crud_handler: Any,
        criteria: dict,
        db_session,
        update_data: dict,
        error_message: str = "Error occurred",
):
    result = await crud_handler.update_one(
        criteria=criteria, db_session=db_session, update_data=update_data,
        collection_name=crud_handler.collection_name
    )

    if result is None:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))

    if result.modified_count != 1:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))

    return result
