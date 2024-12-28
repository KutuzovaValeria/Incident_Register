import pytest
from app import app, db
from flask_sqlalchemy import SQLAlchemy
from models import Incident, Person


@pytest.fixture
def client(mysql):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootpassword@mysql-container:3306/devops'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://std_2641_devops:asdasdasd@std-mysql.ist.mospolytech.ru:3306/std_2641_devops?&collation=utf8mb4_general_ci'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client
        db.session.remove()
        db.drop_all()  


@pytest.fixture
def create_incident():
    def _create_incident(registration_number, registration_date, summary, decision):
        incident = Incident(
            registration_number=registration_number,
            registration_date=registration_date,
            summary=summary,
            decision=decision
        )
        db.session.add(incident)
        db.session.commit()
        return incident
    return _create_incident


@pytest.fixture
def create_person():
    def _create_person(registration_number, first_name, last_name, address, convictions_count=0):
        person = Person(
            registration_number=registration_number,
            first_name=first_name,
            last_name=last_name,
            address=address,
            convictions_count=convictions_count
        )
        db.session.add(person)
        db.session.commit()
        return person
    return _create_person


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Главная страница' in response.data.decode('utf-8')




def test_get_incidents_count(client, create_incident):
    create_incident('001', '2024-12-01', 'Test summary', 'Resolved')
    create_incident('002', '2024-12-02', 'Test summary 2', 'Pending')

    response = client.get('/incidents_count?start_date=2024-12-01&end_date=2024-12-02')
    assert response.status_code == 200
    assert b'2' in response.data  


def test_add_incident(client):
    response = client.post('/add_incident', data={
        'registration_number': '003',
        'registration_date': '2024-12-03',
        'summary': 'Test summary 3',
        'decision': 'Resolved'
    })
    assert response.status_code == 200
    assert b'003' in response.data  


def test_add_person(client, create_person):
    response = client.post('/add_person', data={
        'registration_number': '1001',
        'first_name': 'John',
        'last_name': 'Doe',
        'address': '123 Test St'
    })
    assert response.status_code == 200
    assert b'John' in response.data  
