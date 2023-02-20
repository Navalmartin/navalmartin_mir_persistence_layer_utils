class InvalidObjectIdException(Exception):
    def __init__(self, oid: str):
        self.message = f"The given id {oid} does not represent a valid bson.ObjectId"

    def __str__(self) -> str:
        return self.message
