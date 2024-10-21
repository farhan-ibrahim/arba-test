# arba-test

Python Web Server

Note:
- The application was built originally using SQLite3 for ease of implementation.
Upon deployment, the database is migrated to Firestore (NoSQL). The original API design was not built for NoSQL, which caused some performance issues.
- Things can be improved
  - Using SQL database to optimise the performance or modify the endpoint to make NoSQL query faster

### Create a virtual env

```
python -m venv env
```

### Install dep

```
pip install -r requirements.txt
```

### Create database

```
flask shell

$ from app.models import db
$ db.create_all()
$ exit()
```

OR

```
python database.py
```

### Running app

```
python run.py

```

## DEBUGGING

### To check if the table is created

```
sqlite3 instance/my.db
sql .tables
sql .quit
```

