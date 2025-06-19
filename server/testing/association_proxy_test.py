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

class TestAssociationProxy:
    '''Customer association proxy in models.py'''

    def test_association_proxy_creation(self, test_client):
        with app.app_context():
            c = Customer(name="Proxy Customer")
            i = Item(name="Proxy Item", price=15.0)
            db.session.add_all([c, i])
            db.session.commit()
            
            # Test the association proxy
            c.items.append(i)
            db.session.commit()
            
            assert len(c.reviews) == 1
            assert i in c.items
            assert c.reviews[0].item == i
            assert c.reviews[0].rating == 5  # Default from creator

    def test_multiple_items(self, test_client):
        with app.app_context():
            c = Customer(name="Multi Customer")
            items = [
                Item(name="Item 1", price=10.0),
                Item(name="Item 2", price=20.0),
                Item(name="Item 3", price=30.0)
            ]
            db.session.add_all([c] + items)
            db.session.commit()
            
            c.items.extend(items)
            db.session.commit()
            
            assert len(c.reviews) == 3
            assert len(c.items) == 3
            for item in items:
                assert item in c.items