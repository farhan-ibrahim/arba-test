# ARBA Application

## Overview

The ARBA Application is a Python-based tool designed to manage image posts and associated comments. It provides an intuitive interface for uploading, viewing, and interacting with image posts, along with managing user comments.

## Features

- **Image Management**: Upload and display image posts.
- **Comment System**: Add, view, and manage comments on each post.

## Prerequisites

Before using the ARBA Application, ensure the following:

1. **Python**: Python 3.8 or later is installed.
2. **Dependencies**: Install required Python libraries using the provided `requirements.txt`.

## Installation

1. Clone or download this repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```
# Create virtual env (if needed)
python -m venv env

# Run application
python run.py

```

or Running in docker

```
docker build -t farhan/arba-test-app .
docker images
docker run -p 8080:3000 <image>
```

## Running with local database

```bash
flask shell

$ from app.models import db
$ db.create_all()
$ exit()

OR

python database.py
```

## Example

1. Get all posts
   `{URL}/posts/all`

2. Get post by id
   `{URL}/post/:post_id`

## Debugging

- To check if the table is created

```
sqlite3 instance/my.db
sql .tables
sql .quit
```

Note:

- The application was built originally using SQLite3 for ease of implementation.
  Upon deployment, the database is migrated to Firestore (NoSQL). The original API design was not built for NoSQL, which caused some performance issues.
- Things can be improved
  - Using SQL database to optimise the performance or modify the endpoint to make NoSQL query faster
