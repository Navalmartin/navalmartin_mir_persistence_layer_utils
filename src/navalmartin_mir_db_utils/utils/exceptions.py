class InvalidObjectIdException(Exception):
    def __init__(self, oid: str):
        self.message = f"The given id {oid} does not represent a valid bson.ObjectId"

    def __str__(self) -> str:
        return self.message


class ResourceNotFoundException(Exception):
    def __init__(self, search_criteria: str):
        self.message = f"Resource with search_criteria {search_criteria} not found"

    def __str__(self) -> str:
        return self.message


class ResourceNotUpdatedException(Exception):
    def __init__(self, resource_id: str):
        self.message = f"Resource with id {resource_id} not updated"

    def __str__(self) -> str:
        return self.message


class ResourceExistsException(Exception):
    def __init__(self, resource_id: str):
        self.message = f"Resource with id {resource_id} exists"

    def __str__(self) -> str:
        return self.message

class DBInsertFailedException(Exception):
    def __init__(self, collection_name: str):
        self.message = f"Insert operation failed for collection {collection_name}"

    def __str__(self) -> str:
        return self.message

class DBUpdateFailedException(Exception):
    def __init__(self, collection_name: str):
        self.message = f"Update operation failed for collection {collection_name}"

    def __str__(self) -> str:
        return self.message

