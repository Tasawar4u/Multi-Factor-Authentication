from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mila9970@localhost/mfa_education'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    enrolled_tutorials = db.Column(db.String(200))
    completed_simulations = db.Column(db.String(200))

class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

class Simulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Routes
@app.route('/')
def index():
    tutorials = Tutorial.query.limit(3).all()  # Fetch a few tutorials
    simulations = Simulation.query.limit(3).all()  # Fetch a few simulations
    return render_template('index.html', tutorials=tutorials, simulations=simulations)

@app.route('/tutorials')
def tutorials():
    tutorials = Tutorial.query.all()
    return render_template('tutorials.html', tutorials=tutorials)

@app.route('/simulations')
def simulations():
    simulations = Simulation.query.all()
    return render_template('simulations.html', simulations=simulations)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'enrolled_tutorials': user.enrolled_tutorials,
        'completed_simulations': user.completed_simulations
    } for user in users])

@app.route('/api/tutorials', methods=['GET'])
def get_tutorials_api():
    tutorials = Tutorial.query.all()
    return jsonify([{
        'id': tutorial.id,
        'name': tutorial.name,
        'description': tutorial.description
    } for tutorial in tutorials])

@app.route('/api/simulations', methods=['GET'])
def get_simulations_api():
    simulations = Simulation.query.all()
    return jsonify([{
        'id': simulation.id,
        'name': simulation.name,
        'description': simulation.description
    } for simulation in simulations])

@app.route('/api/mfa/tutorial', methods=['POST'])
def start_tutorial():
    data = request.json
    tutorial_name = data.get('name')
    return jsonify({
        'message': f'Starting tutorial: {tutorial_name}'
    })

@app.route('/api/mfa/simulation', methods=['POST'])
def start_simulation():
    data = request.json
    simulation_name = data.get('name')
    return jsonify({
        'message': f'Starting simulation: {simulation_name}'
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
