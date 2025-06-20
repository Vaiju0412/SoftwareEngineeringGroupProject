from Backend import create_app
from Backend.extensions import db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    insp = inspect(db.engine)
    for fk in insp.get_foreign_keys('user_med_map'):
        print(fk['name'])
