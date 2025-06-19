from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    reviews = db.relationship('Review', backref='customer')
    items = association_proxy('reviews', 'item',
                            creator=lambda item: Review(item=item, rating=5))
    
    serialize_only = ('id', 'name')  # Explicitly specify only these fields
    
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    reviews = db.relationship('Review', backref='item')
    
    serialize_rules = ('-reviews.item',)
    
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    rating = db.Column(db.Integer)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    serialize_rules = ('-customer.reviews', '-item.reviews')
    
    def __repr__(self):
        return f'<Review {self.id}, {self.rating}, {self.comment}>'