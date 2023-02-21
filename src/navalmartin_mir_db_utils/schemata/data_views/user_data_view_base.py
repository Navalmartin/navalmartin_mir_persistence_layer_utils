from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from navalmartin_mir_db_utils.schemata.data_views.indexed_item_data_view_base import IndexedItemDataViewBase


class UserDataViewBase(BaseModel):
    idx: Optional[str] = Field(title="idx",
                               description="The MongoDB index of the item",
                               alias="_id")

    email: Optional[EmailStr] = Field(
        title="email", description="The email of the user"
    )
    name: Optional[str] = Field(title="name", 
                                description="The name of the user")
    surname: Optional[str] = Field(
        title="surname", description="The surname of the user"
    )

    created_at: Optional[str] = Field(
        title="created_at", description="Time and date the particular entry was created"
    )
    updated_at: Optional[str] = Field(
        title="updated_at", description="Time and date the particular entry was updated"
    )

    access_token: Optional[str] = Field(title="access_token", description="The access token assigned to the user")
    refresh_token: Optional[str] = Field(title="refresh_token", description="The access token assigned to the user")

    @staticmethod
    def build_from_mongodb_json(
        mdb_json: dict,
        access_token: str,
        refresh_token: str,
    ) -> "UserDataViewBase":
        """Build the user data from the specified MongoDB document

        Parameters
        ----------
        mdb_json: The MongoDB document
        access_token: The access token
        refresh_token: The refresh token

        Returns
        -------

        """

        mdb_json["index_data"] = IndexedItemDataViewBase.build_from_mongodb_json(mdb_json=mdb_json).dict()

        mdb_json["access_token"] = access_token
        mdb_json["refresh_token"] = refresh_token

        return UserDataViewBase(**mdb_json)
