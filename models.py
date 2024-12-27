from extensions import db

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_number = db.Column(db.String(50), nullable=False, unique=True)
    registration_date = db.Column(db.Date, nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    decision = db.Column(db.String(255), nullable=False)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_number = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    address = db.Column(db.String(255), nullable=False)
    convictions_count = db.Column(db.Integer, default=0)

class IncidentPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)