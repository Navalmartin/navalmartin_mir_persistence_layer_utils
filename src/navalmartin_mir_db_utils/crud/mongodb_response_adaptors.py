from pydantic import BaseModel
from typing import List, Any


class QueryResponseAdaptor:
    @staticmethod
    def adapt_one_model_as_dict(model: BaseModel, exclude_vals: List[Any]) -> dict:

        result = {}

        for item in model.__fields_set__:
            if model.__dict__[item] in exclude_vals:
                continue
            result[item] = model.__dict__[item]
        return result
