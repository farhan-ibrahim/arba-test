from sqlalchemy import inspect
from app.models import db
import app

with app.create_app().app_context():
    db.drop_all()
    db.create_all()

    # Print the table names
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    print(f'<Created {table_names}>')

    print('Database created successfully')