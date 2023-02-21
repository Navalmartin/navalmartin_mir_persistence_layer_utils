from pydantic import BaseModel, Field
from typing import Optional

from navalmartin_mir_db_utils.utils.transform_utils import stringify_dictionary


class IndexedItemDataViewBase(BaseModel):
    idx: Optional[str] = Field(title="idx",
                               description="The MongoDB index of the item",
                               alias="_id")

    created_at: Optional[str] = Field(
        title="created_at", description="Time and date the particular entry was created"
    )
    updated_at: Optional[str] = Field(
        title="updated_at", description="Time and date the particular entry was updated"
    )

    @staticmethod
    def build_from_mongodb_json(
            mdb_json: dict
    ) -> "IndexedItemDataViewBase":
        """Build the user data from the specified MongoDB document

        Parameters
        ----------
        mdb_json: The MongoDB document
        
        Returns
        -------

        """

        data = stringify_dictionary(data=mdb_json,
                                    names=["_id", "created_at", "updated_at"],
                                    )
        return IndexedItemDataViewBase(**data)

