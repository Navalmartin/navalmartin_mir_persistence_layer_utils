import asyncio
import bson
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import ReadEntityCRUDAPI
from navalmartin_mir_db_utils.utils.exceptions import ResourceNotFoundException
from navalmartin_mir_db_utils.crud.crud_utils import get_one_result_or_raise

COLLECTION_NAME = "YOUR_COLLECTION_NAME"
MONGODB_URL = "YOUR_MONGODB_URL"
MONGO_DB_NAME_FROM = "YOUR_MONGODB_NAME"


async def query_db(mongodb_session: MongoDBSession, criteria: dict,
                   projection: dict,
                   collection_name: str):
    query_result = ReadEntityCRUDAPI.find(criteria=criteria, projection=projection,
                                          db_session=mongodb_session,
                                          collection_name=collection_name)
    docs = [doc async for doc in query_result]
    return docs


async def count_docs(mongodb_session: MongoDBSession, criteria: dict,
                     collection_name: str):
    query_result = await ReadEntityCRUDAPI.count_documents(criteria=criteria,
                                                           db_session=mongodb_session,
                                                           collection_name=collection_name)
    return query_result


async def query_db_or_raise(mongodb_session: MongoDBSession, criteria: dict,
                            projection: dict,
                            collection_name: str):
    query_result = await get_one_result_or_raise(crud_handler=ReadEntityCRUDAPI(collection_name=collection_name),
                                                 projection=projection,
                                                 criteria=criteria,
                                                 db_session=mongodb_session)

    return query_result


async def run_examples(mir_db_session_from: MongoDBSession):
    result = await query_db(mongodb_session=mir_db_session_from,
                            criteria={'_id': bson.ObjectId('63ebc9f94c092a48bd179ae7')},
                            projection={},
                            collection_name=COLLECTION_NAME)
    print(result)
    n_docs = await count_docs(mongodb_session=mir_db_session_from,
                              criteria={},
                              collection_name=COLLECTION_NAME)
    print(n_docs)

    try:
        result = await query_db_or_raise(mongodb_session=mir_db_session_from,
                                         criteria={'survey_idx': bson.ObjectId('63ad64252c853ee163fc6a63')},
                                         projection={'original_filename': 1},
                                         collection_name=COLLECTION_NAME)
    except ResourceNotFoundException as e:
        print(str(e))


def main():
    mir_db_session_from = MongoDBSession(mongodb_url=MONGODB_URL,
                                         db_name=MONGO_DB_NAME_FROM)

    asyncio.run(run_examples(mir_db_session_from=mir_db_session_from))

    
if __name__ == '__main__':
    main()
