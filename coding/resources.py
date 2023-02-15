from flask_restful import Resource, reqparse, fields, marshal_with, request

# Import the models from models.py
from models import db, Task, User, Project, Iteration, Tag

# Define the output fields for tasks
task_fields = {
  'id': fields.Integer,
  'title': fields.String,
  'description': fields.String,
  'due_date': fields.String,
  'completed': fields.Boolean,
  'completed_at': fields.String,
  'user_id': fields.Integer,
  'project_id': fields.Integer,
  'iteration_id': fields.Integer,
  'tag_ids': fields.List(fields.Integer)
}

# Define the resource for tasks
class TaskResource(Resource):
  # Define the method for creating a new task
  @marshal_with(task_fields)
  def post(self):
    # Get the JSON data from the request
    data = request.get_json()

    # Create a new task object
    task = Task(
      title=data['title'],
      description=data['description'],
      due_date=data['due_date'],
      completed=data['completed'],
      completed_at=data['completed_at'],
      user_id=data['user_id'],
      project_id=data['project_id'],
      iteration_id=data['iteration_id'],
      tag_ids=data['tag_ids']
    )

    # Add the task to the database
    db.session.add(task)
    db.session.commit()

    # Return the task data
    return task, 201

  # Define the method for querying tasks
  @marshal_with(task_fields)
  def get(self):
    # Get the query parameter from the request
    user_id = request.args.get('user_id')

    # Query the tasks by user id
    if user_id:
      tasks = Task.query.filter_by(user_id=user_id).all()
    else:
      tasks = Task.query.all()

    # Return the tasks data
    return tasks, 200

# Define the resource for a single task
class SingleTaskResource(Resource):
  # Define the method for updating a task
  @marshal_with(task_fields)
  def put(self, task_id):
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
    task.user_id = data['user_id']
    task.project_id = data['project_id']
    task.iteration_id = data['iteration_id']
    task.tag_ids = data['tag_ids']

    # Commit the changes to the database
    db.session.commit()

    # Return the task data
    return task, 200

# Define the output fields for iterations
iteration_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'description': fields.String,
  'start_date': fields.String,
  'end_date': fields.String,
  'project_id': fields.Integer,
  'tasks': fields.List(fields.Nested(task_fields))
}

# Define the output fields for projects
project_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'description': fields.String,
  'start_date': fields.String,
  'end_date': fields.String,
  'user_id': fields.Integer,
  'iterations': fields.List(fields.Nested(iteration_fields)),
  'tasks': fields.List(fields.Nested(task_fields))
}

# Define the output fields for users
user_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'email': fields.String,
  'tasks': fields.List(fields.Nested(task_fields)),
  'projects': fields.List(fields.Nested(project_fields))
}

# Define the resource for users
class UserResource(Resource):
  # Define the method for creating a new user
  @marshal_with(user_fields)
  def post(self):
    # Get the JSON data from the request
    data = request.get_json()

    # Create a new user object
    user = User(
      name=data['name'],
      email=data['email']
    )

    # Add the user to the database
    db.session.add(user)
    db.session.commit()

    # Return the user data
    return user, 201

  # Define the method for querying users
  @marshal_with(user_fields)
  def get(self):
    # Get the query parameter from the request
    email = request.args.get('email')

    # Query the users by email
    if email:
      users = User.query.filter_by(email=email).all()
    else:
      users = User.query.all()

    # Return the users data
    return users, 200

# Define the resource for a single user
class SingleUserResource(Resource):
  # Define the method for updating a user
  @marshal_with(user_fields)
  def put(self, user_id):
    # Get the JSON data from the request
    data = request.get_json()

    # Get the user from the database by id
    user = User.query.get_or_404(user_id)

    # Update the user attributes
    user.name = data['name']
    user.email = data['email']

    # Commit the changes to the database
    db.session.commit()

    # Return the user data
    return user, 200

# Define the resource for projects
class ProjectResource(Resource):
  # Define the method for creating a new project
  @marshal_with(project_fields)
  def post(self):
    # Get the JSON data from the request
    data = request.get_json()

    # Create a new project object
    project = Project(
      name=data['name'],
      description=data['description'],
      start_date=data['start_date'],
      end_date=data['end_date'],
      user_id=data['user_id']
    )

    # Add the project to the database
    db.session.add(project)
    db.session.commit()

    # Return the project data
    return project, 201

  # Define the method for querying projects
  @marshal_with(project_fields)
  def get(self):
    # Get the query parameter from the request
    user_id = request.args.get('user_id')

    # Query the projects by user id
    if user_id:
      projects = Project.query.filter_by(user_id=user_id).all()
    else:
      projects = Project.query.all()

    # Return the projects data
    return projects, 200

# Define the resource for a single project
class SingleProjectResource(Resource):
  # Define the method for updating a project
  @marshal_with(project_fields)
  def put(self, project_id):
    # Get the JSON data from the request
    data = request.get_json()

    # Get the project from the database by id
    project = Project.query.get_or_404(project_id)

    # Update the project attributes
    project.name = data['name']
    project.description = data['description']
    project.start_date = data['start_date']
    project.end_date = data['end_date']
    project.user_id = data['user_id']

    # Commit the changes to the database
    db.session.commit()

    # Return the project data
    return project, 200

# Define the resource for iterations
class IterationResource(Resource):
  # Define the method for creating a new iteration
  @marshal_with(iteration_fields)
  def post(self):
    # Get the JSON data from the request
    data = request.get_json()

  # Create a new iteration object
    iteration = Iteration(
      name=data['name'],
      description=data['description'],
      start_date=data['start_date'],
      end_date=data['end_date'],
      project_id=data['project_id']
    )

    # Add the iteration to the database
    db.session.add(iteration)
    db.session.commit()

    # Return the iteration data
    return iteration, 201

  # Define the method for querying iterations
  @marshal_with(iteration_fields)
  def get(self):
    # Get the query parameter from the request
    project_id = request.args.get('project_id')

    # Query the iterations by project id
    if project_id:
      iterations = Iteration.query.filter_by(project_id=project_id).all()
    else:
      iterations = Iteration.query.all()

    # Return the iterations data
    return iterations, 200

# Define the resource for a single iteration
class SingleIterationResource(Resource):
  # Define the method for updating an iteration
  @marshal_with(iteration_fields)
  def put(self, iteration_id):
    # Get the JSON data from the request
    data = request.get_json()

    # Get the iteration from the database by id
    iteration = Iteration.query.get_or_404(iteration_id)

    # Update the iteration attributes
    iteration.name = data['name']
    iteration.description = data['description']
    iteration.start_date = data['start_date']
    iteration.end_date = data['end_date']
    iteration.project_id = data['project_id']

    # Commit the changes to the database
    db.session.commit()

    # Return the iteration data
    return iteration, 200

# Define the output fields for tags
tag_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'tasks': fields.List(fields.Nested(task_fields))
}

# Define the resource for tags
class TagResource(Resource):
  # Define the method for creating a new tag
  @marshal_with(tag_fields)
  def post(self):
    # Get the JSON data from the request
    data = request.get_json()

    # Create a new tag object
    tag = Tag(
      name=data['name']
    )

    # Add the tag to the database
    db.session.add(tag)
    db.session.commit()

    # Return the tag data
    return tag, 201

  # Define the method for querying tags
  @marshal_with(tag_fields)
  def get(self):
    # Get the query parameter from the request
    name = request.args.get('name')

    # Query the tags by name
    if name:
      tags = Tag.query.filter_by(name=name).all()
    else:
      tags = Tag.query.all()

    # Return the tags data
    return tags, 200

# Define the resource for a single tag
class SingleTagResource(Resource):
  # Define the method for updating a tag
  @marshal_with(tag_fields)
  def put(self, tag_id):
    # Get the JSON data from the request
    data = request.get_json()

    # Get the tag from the database by id
    tag = Tag.query.get_or_404(tag_id)

    # Update the tag attributes
    tag.name = data['name']

    # Commit the changes to the database
    db.session.commit()

    # Return the tag data
    return tag, 200
