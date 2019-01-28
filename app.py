from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# JWT, Json Web Token. We use it as an user id

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # in the root folder where we run the code
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off the Flask one, not the core one
app.secret_key = 'jose'
api = Api(app)

# use thing only from Flask
@app.before_first_request
def create_tables():
    # it only creates all the tables it sees. If no resource is using, you can import model instead
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') 
# now the resource is accessable 
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# We only want to run this when we are running this, not importing this
if __name__ == '__main__': # only the file you run is __main__
    from db import db # import here to prevent circular import. Because model will import db as well
    db.init_app(app)
    app.run(port=5000, debug=True) # show useful error message when set debug=True
