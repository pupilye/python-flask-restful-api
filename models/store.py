from db import db

class StoreModel(db.Model): # define how an item interacts with the internal database
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') # back references, this can be many
    # with lazy='dynamic', it becomes a query builder. And it save resources
    # then every calling of json method need to go through the tables again
    
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name

    def save_to_db(self):
        # serve for both update and insert
        db.session.add(self) # session: the collection of objects to add to the database
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


