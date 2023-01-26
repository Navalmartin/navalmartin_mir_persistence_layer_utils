from typing import Callable, Any
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

from navalmartin_mir_db_utils.dbs.mongodb_session import MongoDBSession
from navalmartin_mir_db_utils.dbs.dbs_utils import DB_ERROR, DB_INFO


async def run_transaction(mdb_session: MongoDBSession,
                          async_callback: Callable,
                          callback_args: dict,
                          max_commit_time_ms: int,
                          read_concern: ReadConcern, write_concern: WriteConcern,
                          read_preference: ReadPreference,
                          with_log: bool = False,
                          transaction_result_handler: Callable = None) -> Any:
    """
    mdb_session: The MongoDB session
    async_callback: The function callback to be used
    callback_args: Dictionary with arguments to pass in the callback
    max_commit_time_ms: The maximum commit time for the transaction
    read_concern: The ReadConcern
    write_concern: The  WriteConcern
    read_preference: The ReadPreference
    with_log: If True it prints information massages on std output
    transaction_result_handler: Callable that specifies how to handle the transaction result

    Returns
    -------

    The transaction result
    """
    try:

        if with_log:
            print(f"{DB_INFO} Starting transaction")

        # Start a client session.
        async with await mdb_session.client.start_session() as session:

            # Use with_transaction to start a transaction,
            # execute the callback, and commit (or abort on error).
            transaction_result = await session.with_transaction(
                lambda s: async_callback(session, callback_args),
                read_concern=read_concern,
                write_concern=write_concern,
                read_preference=read_preference,
                max_commit_time_ms=max_commit_time_ms
            )

            if transaction_result_handler is not None:
                transaction_result = await transaction_result_handler(transaction_result)

        if with_log:
            print(f"{DB_INFO} End transaction")

        return transaction_result
    except Exception as e:
        if with_log:
            print(f"{DB_ERROR} Session with transaction raised an exception. Exception message={str(e)}")
        raise e
