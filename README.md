# arba-test

Python Web Server

### Create virtual env

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

### To check if table is created

```
sqlite3 instance/my.db
sql .tables
sql .quit
```
