from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_migrate import Migrate
from extensions import db
from models import Incident, Person, IncidentPerson

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html', title="Главная страница")

@app.route('/incidents_count', methods=['GET'])
def get_incidents_count():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    count = Incident.query.filter(
        Incident.registration_date.between(start_date, end_date)
    ).count()
    return render_template('/incidents_count.html', start_date=start_date, end_date=end_date, count=count)


@app.route('/person_incidents/<person_id>', methods=['GET'])
def get_person_incidents(person_id):
    count = IncidentPerson.query.filter_by(person_id=person_id).count()
    return render_template('/incidents_of_person.html', count=count)


#@app.route('/person_incidents', methods=['GET', 'POST'])
#def person_incidents():
#    if request.method == 'POST':
#        person_id = request.form['person_id']
#        return redirect(url_for('get_person_incidents', person_id=person_id))
#    return render_template('/person_inc_form')


@app.route('/add_incident', methods=['POST', 'GET'])
def add_incident():
    if request.method == 'POST':
        data = request.form
        new_incident = Incident(
            registration_number=data['registration_number'],
            registration_date=data['registration_date'],
            summary=data['summary'],
            decision=data['decision']
        )
        db.session.add(new_incident)
        db.session.commit()
        return render_template(
            'add_incident.html', 
            registration_number=data['registration_number'],
            registration_date=data['registration_date'],
            summary=data['summary'],
            decision=data['decision']
        )
    return render_template('add_incident.html')



@app.route('/incident/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    data = request.json
    incident = Incident.query.get_or_404(incident_id)
    incident.registration_number = data['registration_number']
    incident.registration_date = data['registration_date']
    incident.summary = data['summary']
    incident.decision = data['decision']
    db.session.commit()
    return jsonify({'message': 'Incident updated successfully'})

@app.route('/add_person', methods=['POST', 'GET'])
def add_person():
    if request.method == 'POST':
        data = request.form
        new_person = Person(
            registration_number=data['registration_number'],
            last_name=data['last_name'],
            first_name=data['first_name'],
            middle_name=data.get('middle_name'),
            address=data['address'],
            convictions_count=data.get('convictions_count', 0)
        )
        db.session.add(new_person)
        db.session.commit()
        
        registration_number = data['registration_number']
        last_name = data['last_name']
        first_name = data['first_name']
        middle_name = data.get('middle_name')
        address = data['address']
        convictions_count = data.get('convictions_count', 0)
        
        return render_template(
            'add_person.html',
            registration_number=registration_number,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            address=address,
            convictions_count=convictions_count
        )
    return render_template('add_person.html')


#@app.route('/person/<int:person_id>', methods=['PUT'])
#def update_person(person_id):
#    data = request.json
#    person = Person.query.get_or_404(person_id)
#    person.registration_number = data['registration_number']
#    person.last_name = data['last_name']
#    person.first_name = data['first_name']
#    person.middle_name = data.get('middle_name')
#    person.address = data['address']
#    person.convictions_count = data['convictions_count']
#    db.session.commit()
#    return jsonify({'message': 'Person updated successfully'})

@app.route('/persons', methods=['GET'])
def persons_list():
    persons = Person.query.all()
    return render_template('persons_list.html', title="Список лиц", persons=persons)

@app.route('/person/<int:person_id>/incidents_count', methods=['GET'])
def person_incidents_count(person_id):
    count = IncidentPerson.query.filter_by(person_id=person_id).count()
    person = Person.query.get_or_404(person_id)
    
    return render_template(
        'person_incidents_count.html',
        title=f"Инциденты для {person.first_name} {person.last_name}",
        person=person,
        count=count
    )
