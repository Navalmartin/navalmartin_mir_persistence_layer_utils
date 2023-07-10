"""module mongodb_crud_utils. Simple utilities
for querying MongoDB

"""
import datetime
from typing import List

from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.utils import InvalidMongoDBOperatorException


class CrudEntityBase(object):

    def __init__(self, collection_name: str):
        self._collection_name = collection_name

    @property
    def collection_name(self) -> str:
        if self._collection_name is None or self._collection_name == "":
            raise ValueError("Collection name is not set")
        return self._collection_name


class CreateEntityCRUDAPI(CrudEntityBase):
    """Create queries in the DB

    """

    def __init__(self, collection_name: str):
        super(CreateEntityCRUDAPI, self).__init__(collection_name)

    @staticmethod
    def insert_one(data: dict, db_session: MongoDBSession, collection_name: str):
        data['created_at'] = datetime.datetime.utcnow()
        data['updated_at'] = datetime.datetime.utcnow()
        result = db_session.db[collection_name].insert_one(data)
        return result

    @staticmethod
    def insert_many(data: List[dict], db_session: MongoDBSession, collection_name: str):
        for item in data:
            item['created_at'] = datetime.datetime.utcnow()
            item['updated_at'] = datetime.datetime.utcnow()

        return db_session.db[collection_name].insert_many(data)


class ReadEntityCRUDAPI(CrudEntityBase):
    """Read queries in the DB

    """

    def __init__(self, collection_name: str):
        super(ReadEntityCRUDAPI, self).__init__(collection_name)

    @staticmethod
    def find(criteria: dict, db_session: MongoDBSession,
             projection: dict,
             collection_name: str):
        result = db_session.db[collection_name].find(criteria, projection=projection)
        return result

    @staticmethod
    def find_one(criteria: dict, db_session: MongoDBSession,
                 projection: dict, collection_name: str):
        result = db_session.db[collection_name].find_one(criteria, projection=projection)
        return result

    @staticmethod
    def count_documents(criteria: dict, db_session: MongoDBSession,
                        collection_name: str):
        result = db_session.db[collection_name].count_documents(criteria)
        return result

    @staticmethod
    def get_distinct(attribute: str, db_session: MongoDBSession,
                     collection_name: str):
        """Returns the distinct occurrences of the attribute
        in the given collection

        Parameters
        ----------
        attribute: The attribute name to get the distinct occurrences'
        db_session: The DB session to use
        collection_name: The collection name to search

        Returns
        -------

        """
        result = db_session.db[collection_name].distinct(attribute)
        return result


class UpdateEntityCRUDAPI(CrudEntityBase):
    """Update queries in the DB

    """

    def __init__(self, collection_name: str):
        super(UpdateEntityCRUDAPI, self).__init__(collection_name)

    @staticmethod
    def update_one(criteria: dict, update_data: dict,
                   db_session: MongoDBSession,
                   collection_name: str,
                   update_op: str = "$set",
                   upsert: bool = False):

        if not update_op.startswith("$"):
            raise InvalidMongoDBOperatorException(operator=update_op,
                                                  extra_message="Operator does not start with '$' ")

        update_data['updated_at'] = datetime.datetime.utcnow()
        result = db_session.db[collection_name].update_one(criteria, {update_op: update_data},
                                                           upsert=upsert)
        return result

    @staticmethod
    def update_many(criteria: dict, update_data: dict,
                    db_session: MongoDBSession,
                    collection_name: str,
                    update_op: str = "$set",
                    upsert: bool = False):

        if not update_op.startswith("$"):
            raise InvalidMongoDBOperatorException(operator=update_op,
                                                  extra_message="Operator does not start with '$' ")

        result = db_session.db[collection_name].update_many(criteria,
                                                            {update_op: update_data},
                                                            upsert=upsert)

        update_data_time = {'updated_at': datetime.datetime.utcnow()}
        return db_session.db[collection_name].update_many(criteria,
                                                          {"$set": update_data_time},
                                                          upsert=upsert)


class DeleteEntityCRUDAPI(CrudEntityBase):
    """Delete queries in the DB

    """

    def __init__(self, collection_name: str):
        super(DeleteEntityCRUDAPI, self).__init__(collection_name)

    @staticmethod
    def delete_one(criteria: dict, db_session: MongoDBSession,
                   collection_name: str):
        result = db_session.db[collection_name].delete_one(criteria)
        return result

    @staticmethod
    def delete_many(criteria: dict, db_session: MongoDBSession, collection_name: str):
        return db_session.db[collection_name].delete_many(criteria)
