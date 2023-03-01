from typing import Any, List


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


class InvalidAttributeValueException(Exception):
    def __init__(self, attribute_name: str, attribute_value: Any, *, allowed_values: List = None,
                 range: tuple = None):
        if allowed_values is not None:
            self.message = f"Attribute {attribute_name} has value {attribute_value} not in {allowed_values}"
        elif range is not None:
            self.message = f"Attribute {attribute_name} has value {attribute_value} not in range [{range[0]}, {range[1]}]"
        else:
            self.message = f"Attribute {attribute_name} has value {attribute_value} which is not valid"
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def __str__(self):
        return self.message


class InvalidMongoDBOperatorException(Exception):
    def __init__(self, operator: str, extra_message: str = ""):
        self.message = f"The operator {operator} is an invalid MongoDB operator"

        if extra_message != "" or extra_message is not None:
            self.message += " " + extra_message

    def __str__(self):
        return self.message

