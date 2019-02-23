from app import app
from db import db

db.init_app(app)


# use thing only from Flask
@app.before_first_request
def create_tables():
    # it only creates all the tables it sees. If no resource is using, you can import model instead
    db.create_all()