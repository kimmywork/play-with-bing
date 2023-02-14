# Import Flask and SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# Create a SQLAlchemy object
db = SQLAlchemy(app)

# Define the models
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)
  tasks = db.relationship('Task', backref='user', lazy=True)
  projects = db.relationship('Project', backref='user', lazy=True)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text)
  due_date = db.Column(db.Date)
  completed = db.Column(db.Boolean, default=False)
  completed_at = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  projects = db.relationship('Project', secondary='project_task', backref='tasks', lazy=True)
  iterations = db.relationship('Iteration', secondary='iteration_task', backref='tasks', lazy=True)
  tags = db.relationship('Tag', secondary='task_tag', backref='tasks', lazy=True)

class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  iterations = db.relationship('Iteration', backref='project', lazy=True)

class Iteration(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=False)
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Tag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  color = db.Column(db.String(10), nullable=False)

# Define the association tables
project_task = db.Table('project_task',
  db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
  db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

iteration_task = db.Table('iteration_task',
  db.Column('iteration_id', db.Integer, db.ForeignKey('iteration.id'), primary_key=True),
  db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

task_tag = db.Table('task_tag',
  db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# Create the database and tables
db.create_all()

# Define the route for creating a new task
@app.route('/tasks', methods=['POST'])
def create_task():
  # Get the JSON data from the request
  data = request.get_json()

  # Create a new task object
  task = Task(
    title=data['title'],
    description=data['description'],
    due_date=data['due_date'],
    user_id=data['user_id'],
    project_id=data['project_id'],
    iteration_id=data['iteration_id'],
    tag_ids=data['tag_ids']
  )

  # Add the task to the database
  db.session.add(task)
  db.session.commit()

  # Return a JSON response with the task data
  return jsonify(task.to_dict()), 201

# Define the route for querying tasks
@app.route('/tasks', methods=['GET'])
def query_tasks():
  # Get the query parameters from the request
  user_id = request.args.get('user_id')
  due_date = request.args.get('due_date')
  completed = request.args.get('completed')
  tag_name = request.args.get('tag_name')

  # Query the tasks based on the parameters
  if user_id:
    tasks = Task.query.filter_by(user_id=user_id).all()
  elif due_date:
    tasks = Task.query.filter_by(due_date=due_date).all()
  elif completed:
    tasks = Task.query.filter_by(completed=completed).all()
  elif tag_name:
    tasks = Task.query.join(task_tag).join(Tag).filter(Tag.name == tag_name).all()
  else:
    tasks = Task.query.all()

  # Return a JSON response with the tasks data
  return jsonify([task.to_dict() for task in tasks]), 200

# Define the route for updating a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
  # Get the JSON data from the request
  data = request.get_json()

  # Get the task from the database by id
  task = Task.query.get_or_404(task_id)

  # Update the task attributes
  task.title = data['title']
  task.description = data['description']
  task.due_date = data['due_date']
  task.completed = data['completed']
  task.completed_at = data['completed_at']

  # Commit the changes to the database
  db.session.commit()

  # Return a JSON response with the task data
  return jsonify(task.to_dict()), 200    