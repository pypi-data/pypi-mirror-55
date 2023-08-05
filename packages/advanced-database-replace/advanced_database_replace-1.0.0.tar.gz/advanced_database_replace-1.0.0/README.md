# Advanced Database Replace


#### Short description
A utility management library which runs an advanced
search&replace action against a specified database's records 
(event if they are serialized).

#### Long description
This project aims to take search&replace to the next level by applying
search&replace even to serialized records in the database. This type of project
is especially effective against e.g. Wordpress databases since they may 
contain serialized PHP array records.

## Prerequisites

- A MySql database.
- This project installed with:
```bash
pip install advanced_database_replace
```
or:
```bash
./install.sh
```

## Usage

#### Replacing all occurrences on all tables
```python
from advanced_database_replace.database_replace import DatabaseReplace
from advanced_database_replace.database_credentials import DatabaseCredentials

db_credentials = DatabaseCredentials()
db_replacer = DatabaseReplace(credentials=db_credentials)

db_replacer.replace_all('my-old-record', 'my-new-record')
```

#### Replacing all occurrences on a specific table
```python
from advanced_database_replace.database_replace import DatabaseReplace
from advanced_database_replace.database_credentials import DatabaseCredentials

db_credentials = DatabaseCredentials()
db_replacer = DatabaseReplace(credentials=db_credentials)

db_replacer.replace('my-old-record', 'my-new-record', 'my-table')
```

#### Using custom serializer
Since (as mentioned in the description) this find&replace project handles serialized
data, by default it assumes PHP serialization, however, you can provide a custom
serializer.

```python
from advanced_database_replace.database_replace import DatabaseReplace
from advanced_database_replace.database_credentials import DatabaseCredentials

class MyCustomSerializer:
    @staticmethod
    def dumps(*args, **kwargs):
        pass
        
    @staticmethod
    def loads(*args, **kwargs):
        pass

db_credentials = DatabaseCredentials()
db_replacer = DatabaseReplace(credentials=db_credentials, serializer=MyCustomSerializer())

db_replacer.replace_all('my-old-record', 'my-new-record')
```