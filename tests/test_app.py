import pytest
from app import create_app
from app.models import db, Ticket

@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / 'test.db'
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + str(db_path), 'SECRET_KEY': 'test'})
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

def login(client):
    return client.post('/login', data={'email':'admin@example.com','password':'admin123'}, follow_redirects=True)

def test_login(client):
    response = login(client)
    assert response.status_code == 200
    assert b'Customer Support Dashboard' in response.data

def test_api_kpis(client):
    login(client)
    response = client.get('/api/kpis')
    assert response.status_code == 200
    assert response.json['total'] >= 8

def test_prediction(client):
    response = client.post('/api/predict', json={'text':'I am very frustrated because the issue is still not fixed'})
    assert response.status_code == 200
    assert response.json['sentiment'] in ['Positive','Negative','Neutral']
