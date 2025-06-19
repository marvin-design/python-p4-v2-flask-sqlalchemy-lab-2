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

class TestReview:
    '''Review model in models.py'''

    def test_review_creation(self, test_client):
        with app.app_context():
            c = Customer(name="Test Customer")
            i = Item(name="Test Item", price=10.0)
            db.session.add_all([c, i])
            db.session.commit()
            
            r = Review(comment="Great product!", rating=5, customer=c, item=i)
            db.session.add(r)
            db.session.commit()
            
            assert r.id is not None
            assert r.comment == "Great product!"
            assert r.rating == 5
            assert r.customer_id == c.id
            assert r.item_id == i.id
            assert r in c.reviews
            assert r in i.reviews

    def test_review_relationships(self, test_client):
        with app.app_context():
            c = Customer(name="Another Customer")
            i = Item(name="Another Item", price=20.0)
            r = Review(comment="Awesome!", rating=4, customer=c, item=i)
            
            db.session.add_all([c, i, r])
            db.session.commit()
            
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews