from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource): # Inherit from the class Resource
# no need to jsonify as flask-restful does it for us
    parser = reqparse.RequestParser() # no this, to make the parser belongs to class itself, not the instances
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 # this is a bad request
         
        data = Item.parser.parse_args() # parse the request payload that go through

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except Exception:
            return {"message": "An error occureed inserting the item."}, 500 # internal server error  

        return item.json(), 201 # 201 is for created
        # 202 is accepted, when you need to delay the creation

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item is not found '}

    def put(self, name): # put is an idempotent request
        data = Item.parser.parse_args() # parse the request payload that go through

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured upsertng the item."}, 500
        
        return item.json(), 201


# class should be separated by two new lines
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} # array interpretation
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}