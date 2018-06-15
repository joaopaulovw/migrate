# Migrate

Migrate it is a software to migrate data between databases.

# Config

This file is used to set the configuration parameters for execution of software.

Config file exemple:

```
{
  "connections": {
    "from": {
      "user": "user",
      "password": "password",
      "host": "host",
      "database": "database"
    },
    "to": {
      "user": "user",
      "password": "password",
      "host": "host",
      "database": "database"
    },
    ...
  },
  "scheme": "scheme.json"
}
```
# Scheme

The scheme it is a file to place what tables and rows you want to migrate.

Scheme file exemple:

```
[
  {
    "table": "addresses",
    "columns": [
      "id",
      "city_id",
      "user_id",
      "street",
      "number",
      "complement",
      "neighborhood",
      "zip_code",
      "formatted_address",
      "lat",
      "lng"
    ]
  },
  {
    "table": "users",
    "columns": [
      "id",
      "name",
      "email",
      "password"
    ]
  },
  ...
]
```

# Run

To run this software you will need to do some thing like this:

```
migrate -f from -t to
```
