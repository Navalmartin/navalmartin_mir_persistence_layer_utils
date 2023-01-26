import asyncio
import bson
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.crud.mongodb_crud_utils import ReadEntityBaseCRUDAPI


IMAGES_COLLECTION_TO_READ = 'YOUR_COLLECTION_NAME'


async def query_db(mongodb_session: MongoDBSession, criteria: dict,
                   projection: dict,
                   collection_name: str):
    query_result = ReadEntityBaseCRUDAPI.do_find(criteria=criteria, projection=projection,
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
