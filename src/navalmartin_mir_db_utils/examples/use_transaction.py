from typing import Any
import bson
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
import asyncio

from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.transanctions import run_transaction
from navalmartin_mir_db_utils.transanctions.decorators import use_async_transaction, with_transaction

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

    print("Running transaction...")
    transaction_result = asyncio.run(execute_function(mir_db_session=mir_db_session))
    print(transaction_result)

    print("Running transaction as decorator...")
    transaction_result = asyncio.run(query_db(mongodb_session=mir_db_session))
    print(transaction_result)
