"""module mongodb_session. Create a session for the MongoDB

"""
import os
import datetime
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure
from typing import Union, Dict, Any, Tuple

from navalmartin_mir_db_utils.dbs.dbs_utils import DB_ERROR


class MongoDBSession(object):

    @classmethod
    def build_with_arguments(cls, mongodb_url: str, db_name: str, **kwargs) -> "MongoDBSession":
        """Build a MongoDBSession with provided arguments. For a list
        of arguments check https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client.html

        Parameters
        ----------
        mongodb_url: The MongoDB URL to use
        db_name: The database name to connect to
        kwargs: The arguments to use

        Returns
        -------

        An instance of MongoDBSession
        """

        db_session = MongoDBSession(mongodb_url=mongodb_url,
                                    db_name=db_name,
                                    build_client=False)

        db_session.client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url, **kwargs)
        db_session.db = db_session.client[db_name]
        return db_session

    def __init__(self, mongodb_url: str = "", db_name: str = "",
                 build_client: bool = True, **kwargs: dict):
        self.mongodb_url: Union[str, None] = mongodb_url
        self.db_name: Union[str, None] = db_name
        self.client = None
        self.db = None

        if build_client:
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

            self.client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(self.mongodb_url, **kwargs)

            # getting a reference to a database
            # does no I/O and does not require an await expression.
            # see: https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
            self.db = self.client[self.db_name]

    def ping(self):
        try:
            # The ping command is cheap and does not require auth.
            self.client.admin.command('ping')
        except ConnectionFailure:
            print("Server not available")

    def close(self) -> None:
        """Closes the connection with the DB.
        See https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client.html
        Cleanup client resources and disconnect from MongoDB.

        End all server sessions created by this client by sending one or more endSessions commands.

        Close all sockets in the connection pools and stop the monitor threads.

        """
        var = self.client.close

    def address(self) -> Tuple:
        """Returns (host, port) of the current standalone, primary, or mongos, or None.
        Accessing address raises InvalidOperation if
        the client is load-balancing among mongoses, since
        there is no single address. Use nodes instead.

        If the client is not connected, this will block until a
        connection is established or
        raise ServerSelectionTimeoutError if no server is available.

        """
        return self.client.address

    async def drop_database(self) -> None:
        """Drop the database that the underlying client is using
        """
        await self.client.drop_database(self.db_name)

    async def get_server_info(self) -> Dict[str, Any]:
        """Returns the DB server information the client
        is connected to
        """
        info = await self.client.server_info()
        return info

    async def insert_one(self, data: Dict, collection_name: str):
        data['created_at'] = datetime.datetime.utcnow()
        data['updated_at'] = datetime.datetime.utcnow()
        result = await self.db[collection_name].insert_one(data)
        return result

    async def find_one(self, criteria: Dict, projection: dict, collection_name: str):
        result = await self.db[collection_name].find_one(criteria, projection=projection)
        return result

    def find(self, criteria: Dict, projection: Dict, collection_name: str):
        result = self.db[collection_name].find(criteria, projection=projection)
        return result


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
