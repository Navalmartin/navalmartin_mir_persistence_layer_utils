import asyncio
import bson
from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.crud.mongodb_crud_ops import ReadEntityCRUDAPI, CreateEntityCRUDAPI
from navalmartin_mir_db_utils.utils.exceptions import ResourceNotFoundException
from navalmartin_mir_db_utils.crud.crud_utils import get_one_result_or_raise

COLLECTION_NAME = "individuals"
MONGODB_URL = "mongodb://localhost:27021/?replicaSet=mongo-mir-app-set"
MONGO_DB_NAME = "MyDb"

async def run_examples(mir_db_session: MongoDBSession) -> None:

    # insert some data
    response = await CreateEntityCRUDAPI.insert_one(data={"name": "John", "surname": "Doe",
                                                          "city":"SunCity",
                                                          "address": "54 JohnDoe highway"},
                                                    collection_name=COLLECTION_NAME,
                                                    db_session=mir_db_session)

    # get the result back
    read_response = await ReadEntityCRUDAPI.find_one(criteria={'_id': response.inserted_id},
                                                 collection_name=COLLECTION_NAME,
                                                 db_session=mir_db_session,
                                                 projection={})

    print(f"Inserted document {read_response}")
    print("Dropping database")
    await mir_db_session.drop_database()



def main():

    mir_db_session = MongoDBSession(mongodb_url=MONGODB_URL,
                                    db_name=MONGO_DB_NAME,
                                    **{'directConnection': True,
                                       'serverSelectionTimeoutMS': 5})

    print(f"Session to database: {mir_db_session.db_name}")
    print(f"Database: {mir_db_session.mongodb_url}")


    asyncio.run(run_examples(mir_db_session=mir_db_session))

    
if __name__ == '__main__':
    main()
