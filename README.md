# mir-persistence-layer-utils

Utilities for the persistence layer when working with the _mir_ project. The official
PyPi package can be found <a href="https://pypi.org/project/navalmartin-mir-db-utils/">here</a>.

## Dependencies

- pymongo
- motor
- bcrypt
- pydantic
- httpx
- hurry.filesize
- python-dotenv

## Installation

Installing the utilities via ```pip```

```
pip install navalmartin-mir-db-utils
```

For a specific version you can use

```
pip install navalmartin-mir-db-utils==x.x.x
```

You can uninstall the project via

```commandline
pip uninstall navalmartin_mir_db_utils
```

## How to use

Create a session

```
from dotenv import load_dotenv
from navalmartin_mir_db_utils.dbs import MongoDBSession 

# laod configuration variables
# using the default .env

# load the MONGODB_URL
load_dotenv()

# assume that the MONGODB_NAME is not loaded
# so we need to set it manuall
session = MongoDBSession(db_name="my-db-name")

```

You can use the session to execute simple queries as shown below

```
import asyncio
import bson
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.crud.mongodb_crud_utils import ReadEntityCRUDAPI

IMAGES_COLLECTION_TO_READ="YOUR_COLLECTION_NAME"


async def query_db(mongodb_session: MongoDBSession, criteria: dict,
                   projection: dict,
                   collection_name: str):
    query_result = ReadEntityCRUDAPI.do_find(criteria=criteria, projection=projection,
                                                 db_session=mongodb_session,
                                                 collection_name=collection_name)
    images = [img async for img in query_result]
    return images
    
    
def main():
    MONGODB_URL = "YOUR_MONGODB_URL"
    MONGO_DB_NAME_FROM = "YOUR_MONGODB_NAME"
    mir_db_session_from = MongoDBSession(mongodb_url=MONGODB_URL,
                                         db_name=MONGO_DB_NAME_FROM)

    result = asyncio.run(query_db(mongodb_session=mir_db_session_from,
                                  criteria={'survey_idx': bson.ObjectId('63ad64252c853ee163fc6a63')},
                                  projection={'original_filename': 1},
                                  collection_name=IMAGES_COLLECTION_TO_READ))
    print(result)
    
if __name__ == '__main__':
    main()
```

You can also run transactions.

```
from typing import Any
import bson
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
import asyncio

from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.transanctions import run_transaction
from navalmartin_mir_db_utils.transanctions.decorators import with_transaction

IMAGES_COLLECTION_TO_READ = "YOUR_COLLECTION_NAME"
MONGODB_URL = "YOUR_MONGODB_URL"
MONGO_DB_NAME_FROM = "YOUR_MONGODB_NAME"

wc_majority = WriteConcern("majority", wtimeout=1000)
read_concern = ReadConcern("local")


async def read_images_callback(session: Any, kwargs: dict):
    db_name = kwargs['db_name']
    survey_idx = kwargs['survey_idx']
    projection = kwargs['projection']

    db = session.client.get_database(db_name)
    images_collection = db[IMAGES_COLLECTION_TO_READ]

    images = images_collection.find({'survey_idx': bson.ObjectId(survey_idx)},
                                    projection=projection,
                                    session=session)
    return images


async def transaction_result_handler(transaction_result: Any):
    images = [img async for img in transaction_result]
    return images
    
@with_transaction
async def execute_function(mir_db_session: MongoDBSession):
    return await run_transaction(mdb_session=mir_db_session,
                                 async_callback=read_images_callback,
                                 callback_args=callback_args,
                                 max_commit_time_ms=None,
                                 read_concern=read_concern,
                                 write_concern=wc_majority,
                                 read_preference=ReadPreference.PRIMARY,
                                 with_log=True,
                                 transaction_result_handler=transaction_result_handler)


if __name__ == '__main__':
    mir_db_session = MongoDBSession(mongodb_url=MONGODB_URL,
                                    db_name=MONGO_DB_NAME_FROM)

    callback_args = {'db_name': 'mir_db',
                     'survey_idx': '63ad64252c853ee163fc6a63',
                     'projection': {'original_filename': 1}}
    transaction_result = asyncio.run(execute_function(mdb_session=mir_db_session))
    print(transaction_result)

```

There is also a decorator available to run a transaction

```
from typing import Any
import bson
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
import asyncio

from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.transanctions.decorators import use_async_transaction

IMAGES_COLLECTION_TO_READ = 'YOUR_COLLECTION_NAME'
MONGODB_URL = "YOUR_MONGODB_URL"
MONGO_DB_NAME_FROM = "YOUR_MONGODB_NAME"

wc_majority = WriteConcern("majority", wtimeout=1000)
read_concern = ReadConcern("local")

callback_args = {'db_name': 'mir_db',
                 'survey_idx': '63ad64252c853ee163fc6a63',
                 'projection': {'original_filename': 1}}


async def read_images_callback(session: Any, kwargs: dict):
    db_name = kwargs['db_name']
    survey_idx = kwargs['survey_idx']
    projection = kwargs['projection']

    db = session.client.get_database(db_name)
    images_collection = db[IMAGES_COLLECTION_TO_READ]

    images = images_collection.find({'survey_idx': bson.ObjectId(survey_idx)},
                                    projection=projection,
                                    session=session)
    return images


async def transaction_result_handler(transaction_result: Any):
    images = [img async for img in transaction_result]
    return images


@use_async_transaction(async_callback=read_images_callback,
                        callback_args=callback_args,
                        mdb_session=MongoDBSession(mongodb_url=MONGODB_URL, db_name=MONGO_DB_NAME_FROM),
                        write_concern=wc_majority,
                        read_concern=read_concern,
                        read_preference=ReadPreference.PRIMARY,
                        max_commit_time_ms=None,
                        with_log=True,
                        with_transaction_result=True,
                        transaction_result_handler=transaction_result_handler)
async def query_db(mongodb_session: MongoDBSession, **kwargs):
    transaction_result = kwargs['transaction_result']
    return transaction_result


if __name__ == '__main__':
    mir_db_session_from = MongoDBSession(mongodb_url=MONGODB_URL,
                                         db_name=MONGO_DB_NAME_FROM)

 
    print("Running transaction as decorator...")
    transaction_result = asyncio.run(query_db(mongodb_session=mir_db_session_from))
    print(transaction_result)

```


