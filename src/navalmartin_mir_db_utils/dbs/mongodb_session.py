"""module mongodb_session. Create a session for the MongoDB

"""
import os

import motor.motor_asyncio
from typing import Union

from navalmartin_mir_db_utils.dbs.dbs_utils import DB_ERROR


class MongoDBSession(object):
    def __init__(self, mongodb_url: str = "", db_name: str = ""):
        self.mongodb_url: Union[str | None] = mongodb_url
        self.db_name: Union[str | None] = db_name
        self.client = None
        self.db = None

        if self.mongodb_url == "" or self.mongodb_url is None:
            self.mongodb_url = os.getenv("MONGODB_URL")

        if self.mongodb_url is None or self.mongodb_url == "":
            print(f"{DB_ERROR} The MongoDB URL is None or empty. Check your configuration")
            raise ValueError("MongoDB URL is not set")

        if self.db_name == "" or self.db_name is None:
            self.db_name = os.getenv("MONGODB_NAME")

        if self.db_name is None or self.db_name == "":
            print(f"{DB_ERROR} The DB name is None or empty. Check your configuration")
            raise ValueError("DB name is not set")

        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongodb_url)
        self.db = self.client[self.db_name]


def get_db_session() -> MongoDBSession:
    """Get an instance of MongoDBSession. The application
    should load the environment variables 'MONGODB_URL' and
    'MONGODB_NAME'

    Returns
    -------

    """
    return MongoDBSession()


def get_db_session_with_config(config: dict) -> MongoDBSession:
    mongodb_url = config['MONGODB_URL']
    db_name = config['MONGODB_NAME']
    return MongoDBSession(mongodb_url=mongodb_url, db_name=db_name)


