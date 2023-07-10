"""index_utils Various utilities for working with indexes with mongodb

"""
from navalmartin_mir_db_utils.dbs import MongoDBSession


async def create_collection_index(attribute_name: str,
                                  db_session: MongoDBSession,
                                  collection_name: str,
                                  unique_index: bool = True) -> str:
    """Create an index on the attribute for the given collection

    Parameters
    ----------
    attribute_name: The attribute name to create the index
    db_session: The active database session
    collection_name: The collection name to impose the index on
    unique_index: Whether the index should be unique

    Returns
    -------

    A string with the response of the DB server
    """
    response = await db_session.db[collection_name].create_index(
        keys=attribute_name, unique=unique_index
    )

    return response