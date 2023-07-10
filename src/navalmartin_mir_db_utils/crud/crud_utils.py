from typing import Any, Callable
from pymongo.results import InsertOneResult, UpdateResult

from navalmartin_mir_db_utils.dbs.dbs_utils import DB_ERROR
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import ReadEntityCRUDAPI, CreateEntityCRUDAPI, UpdateEntityCRUDAPI
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.utils.exceptions import (ResourceNotFoundException, ResourceNotUpdatedException,
                                                       ResourceExistsException, DBInsertFailedException)


async def get_one_result_or_raise(
        crud_handler: ReadEntityCRUDAPI,
        criteria: dict,
        db_session: MongoDBSession,
        projection: dict = {},
        error_message: str = "Error occurred"
) -> Any:
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


async def insert_one_or_fail(crud_handler: CreateEntityCRUDAPI,
                             insert_data: dict,
                             db_session: MongoDBSession,
                             error_message: str = "Error occurred",
                             schema: Callable = None) -> InsertOneResult:
    """Insert one document in the collection that the crud handler
    manipulates

    Parameters
    ----------
    crud_handler: The handler that does the insert
    insert_data: The data to insert
    db_session: The active database session
    error_message: The error message to show if insertion fails
    schema: The schema to validate the data
    Returns
    -------

    An instance of InsertOneResult
    """

    if schema is not None:
        try:
            schema(**insert_data)
        except Exception as e:
            print(f"{DB_ERROR} Schema validation failed on insert")
            raise DBInsertFailedException(collection_name=crud_handler.collection_name)

    result: InsertOneResult = await crud_handler.insert_one(data=insert_data,
                                                            db_session=db_session,
                                                            collection_name=crud_handler.collection_name)

    if result is None:
        print(f"{DB_ERROR} {error_message}")
        raise DBInsertFailedException(collection_name=crud_handler.collection_name)

    if not result.acknowledged:
        print(f"{DB_ERROR} {error_message}")
        raise DBInsertFailedException(collection_name=crud_handler.collection_name)

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
        crud_handler: UpdateEntityCRUDAPI,
        criteria: dict,
        db_session,
        update_data: dict,
        update_op: str = "$set",
        error_message: str = "Error occurred",
) -> UpdateResult:
    result: UpdateResult = await crud_handler.update_one(
        criteria=criteria, db_session=db_session, update_data=update_data,
        collection_name=crud_handler.collection_name, update_op=update_op
    )

    if result is None:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))

    if not result.acknowledged:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))


    """
    if result.modified_count != 1:
        print(f"{DB_ERROR} {error_message}")
        raise ResourceNotUpdatedException(resource_id=str(criteria))
    """

    return result
