import datetime
from navalmartin_mir_db_utils.schemata import IndexedItemDataViewBase, UserDataViewBase


class MyIndexedItem(IndexedItemDataViewBase):
    pass


if __name__ == '__main__':
    mdb_json = {'_id': '123456',
                'created_at': datetime.datetime.utcnow(),
                'updated_at': datetime.datetime.utcnow()}

    my_indexed_item = MyIndexedItem.build_from_mongodb_json(mdb_json=mdb_json)

    print(f"MyIndexedItem  {my_indexed_item}")
    print(f"MyIndexedItem fields set {my_indexed_item.__fields_set__}")

    user_data_json = {'_id': '123456',
                      'created_at': datetime.datetime.utcnow(),
                      'updated_at': datetime.datetime.utcnow(),
                      "name": "Alex",
                      "surname": "Giavaras",
                      "email": "alex@someemail.com"}

    user = UserDataViewBase.build_from_mongodb_json(mdb_json=user_data_json,
                                                    access_token="1236",
                                                    refresh_token="69878")

    print(f"User  {user}")
    print(f"User fields set {user.__fields_set__}")
