# mir-persistence-layer-utils

Utilities for the persistence layer when working with the _mir_ project

## Dependencies

- pymongo
- motor
- bcrypt
- pydantic
- httpx
- hurry.filesize
- python-dotenv
- 
## Installation

Installing the utilities via ```pip```

```
pip install -i https://test.pypi.org/simple/ navalmartin-mir-db-utils
```

Notice that the project is pulled from ```TestPyPi``` which does not have the same packages
as the official PyPi index. This means that dependencies may fail to install. It is advised therefore
to manually install the dependencies mentioned above.

You can uninstall the project via

```commandline
pip3 uninstall navalmartin_mir_db_utils
```

## How to use

```
from dotenv import load_dotenv
from navalmartin_mir_db_utils.dbs import MongoDBSession 

# laod configuration variables
# using the default .env

# load the MONGODB_URL
load_dotenv()

# assume that the MONGODB_NAME is not loaded
# so we need to set it manuall
session = MongoDBSession(db_name="my-db-name")
```


