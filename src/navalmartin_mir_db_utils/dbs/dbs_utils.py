import bson
from navalmartin_mir_db_utils.utils.exceptions import InvalidObjectIdException

INVALID_BSON_ID = "INVALID_BSON_OBJ_ID"

DB_INFO = "DB_INFO: "
DB_WARNING = "DB_WARNING: "
DB_ERROR = "DB_ERROR: "


def is_valid_object_id(oid: str) -> bson.ObjectId:
    """Attempts to change the given oid in a valid bson.ObjectId.
    It raises InvalidObjectIdException if the cast fials
    Paramaters
    ----------
    oid: The object id to check

    Returns
    -------

    An instance of bson.ObjectId upon successfully casting the oid in 
    a bson.ObjectId
    """
    try:
        oid = bson.ObjectId(oid)
        return oid
    except Exception as e:
        raise InvalidObjectIdException(oid=oid)
