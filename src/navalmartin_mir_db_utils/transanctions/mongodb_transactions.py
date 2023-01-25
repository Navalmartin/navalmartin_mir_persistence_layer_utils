from functools import wraps
from typing import Callable
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

from mir_persistence_layer_utils.dbs.mongodb_session import MongoDBSession


def with_transaction(mdb_session: MongoDBSession, fn: Callable,
                     callback: Callable, max_commit_time_ms: int,
                     read_concern: ReadConcern, write_concern: WriteConcern,
                     read_preference: ReadPreference):
    """Decorator to wrap the given callable into a MongoDB transaction
    The callback function implements the actual read/write operations

    Parameters
    ----------
    mdb_session: The MongoDB session
    fn: The function to wrap
    callback: The function callback to be used
    max_commit_time_ms: The maximum commit time for the transaction
    read_concern: The ReadConcern
    write_concern: The  WriteConcern
    read_preference: The ReadPreference
    Returns
    -------

    """
    @wraps(fn)
    def wrapper(*args, **kwargs):

        # Start a client session.
        with mdb_session.client.start_session() as session:
            # Use with_transaction to start a transaction,
            # execute the callback, and commit (or abort on error).
            session.with_transaction(
                callback,
                read_concern=read_concern,
                write_concern=write_concern,
                read_preference=read_preference,
                max_commit_time_ms=max_commit_time_ms
            )

        return fn(*args, **kwargs)
    return wrapper


def with_async_transaction(mdb_session: MongoDBSession, async_fn: Callable,
                           async_callback: Callable, max_commit_time_ms: int,
                           read_concern: ReadConcern, write_concern: WriteConcern,
                           read_preference: ReadPreference):
    """Decorator to wrap the given callable into a MongoDB transaction
    The callback function implements the actual read/write operations.
    This is similar to with_transaction but assumes async ops

    Parameters
    ----------
    mdb_session: The MongoDB session
    async_fn: The function to wrap
    async_callback: The function callback to be used
    max_commit_time_ms: The maximum commit time for the transaction
    read_concern: The ReadConcern
    write_concern: The  WriteConcern
    read_preference: The ReadPreference

    Returns
    -------

    """
    @wraps(async_fn)
    async def wrapper(*args, **kwargs):
        # Start a client session.
        async with await mdb_session.client.start_session() as session:
            # Use with_transaction to start a transaction,
            # execute the callback, and commit (or abort on error).
            await session.with_transaction(
                async_callback,
                read_concern=read_concern,
                write_concern=write_concern,
                read_preference=read_preference,
                max_commit_time_ms=max_commit_time_ms
            )

        return await async_fn(*args, **kwargs)

    return wrapper

