# Import SQLAlchemy and Flask-SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy object
db = SQLAlchemy()

# Define the many-to-many association table for tasks and tags
task_tag = Table('task_tag', db.Model.metadata,
  Column('task_id', Integer, ForeignKey('task.id')),
  Column('tag_id', Integer, ForeignKey('tag.id'))
)

# Define the Task model
class Task(db.Model):
  # Define the table name
  __tablename__ = 'task'

  # Define the columns
  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  description = Column(String(500), nullable=True)
  due_date = Column(DateTime, nullable=True)
  completed = Column(Boolean, default=False)
  completed_at = Column(DateTime, nullable=True)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
  project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
  iteration_id = Column(Integer, ForeignKey('iteration.id'), nullable=False)
  tag_ids = Column(db.ARRAY(Integer), nullable=True)

  # Define the relationships
  user = relationship('User', back_populates='tasks')
  project = relationship('Project', back_populates='tasks')
  iteration = relationship('Iteration', back_populates='tasks')
  tags = relationship('Tag', secondary=task_tag, back_populates='tasks')

  # Define the method for converting the object to a dictionary
  def to_dict(self):
    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'due_date': self.due_date,
      'completed': self.completed,
      'completed_at': self.completed_at,
      'user_id': self.user_id,
      'project_id': self.project_id,
      'iteration_id': self.iteration_id,
      'tag_ids': self.tag_ids
    }

# Define the User model
class User(db.Model):
  # Define the table name
  __tablename__ = 'user'

  # Define the columns
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  email = Column(String(100), nullable=False, unique=True)

  # Define the relationships
  tasks = relationship('Task', back_populates='user')
  projects = relationship('Project', back_populates='user')

  # Define the method for converting the object to a dictionary
  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email,
      'tasks': [task.to_dict() for task in self.tasks],
      'projects': [project.to_dict() for project in self.projects]
    }

# Define the Project model
class Project(db.Model):
  # Define the table name
  __tablename__ = 'project'

  # Define the columns
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  description = Column(String(500), nullable=True)
  start_date = Column(DateTime, nullable=True)
  end_date = Column(DateTime, nullable=True)
  user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

  # Define the relationships
  user = relationship('User', back_populates='projects')
  iterations = relationship('Iteration', back_populates='project')
  tasks = relationship('Task', back_populates='project')

  # Define the method for converting the object to a dictionary
  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'user_id': self.user_id,
      'iterations': [iteration.to_dict() for iteration in self.iterations],
      'tasks': [task.to_dict() for task in self.tasks]
    }

# Define the Iteration model
class Iteration(db.Model):
  # Define the table name
  __tablename__ = 'iteration'

  # Define the columns
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  description = Column(String(500), nullable=True)
  start_date = Column(DateTime, nullable=True)
  end_date = Column(DateTime, nullable=True)
  project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
  # Define the relationships
  project = relationship('Project', back_populates='iterations')
  tasks = relationship('Task', back_populates='iteration')

  # Define the method for converting the object to a dictionary
  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'project_id': self.project_id,
      'tasks': [task.to_dict() for task in self.tasks]
    }

# Define the Tag model
class Tag(db.Model):
  # Define the table name
  __tablename__ = 'tag'

  # Define the columns
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False, unique=True)

  # Define the relationships
  tasks = relationship('Task', secondary=task_tag, back_populates='tags')

  # Define the method for converting the object to a dictionary
  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'tasks': [task.to_dict() for task in self.tasks]
    }