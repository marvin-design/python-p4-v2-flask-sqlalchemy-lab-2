import pytest
from server.app import app, db
from server.models import Customer, Item, Review

@pytest.fixture(scope='module')
def test_client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

class TestSerialization:
    '''Model serialization in models.py'''

    def test_customer_serialization(self, test_client):
        with app.app_context():
            c = Customer(name="Serial Customer")
            db.session.add(c)
            db.session.commit()
            
            serialized = c.to_dict()
            assert serialized['id'] == c.id
            assert serialized['name'] == "Serial Customer"
            assert 'reviews' not in serialized  # Check rules are working

    def test_review_serialization(self, test_client):
        with app.app_context():
            c = Customer(name="Review Customer")
            i = Item(name="Review Item", price=25.0)
            r = Review(comment="Test review", rating=3, customer=c, item=i)
            
            db.session.add_all([c, i, r])
            db.session.commit()
            
            serialized = r.to_dict()
            assert serialized['comment'] == "Test review"
            assert serialized['rating'] == 3
            assert 'customer' in serialized
            assert 'item' in serialized
            assert 'reviews' not in serialized['customer']  # Check rules