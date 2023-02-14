
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