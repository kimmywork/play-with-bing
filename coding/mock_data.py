# Import the models and the database from models.py
from models import db, User, Project, Iteration, Task, Tag

# Import the Faker library
from faker import Faker

# Create a Faker instance
fake = Faker()

# Create some fake users
users = []
for i in range(10):
  user = User(
    name=fake.name(),
    email=fake.email()
  )
  users.append(user)
db.session.add_all(users)


# Create some fake projects
projects = []
for i in range(5):
  project = Project(
    name=fake.sentence(),
    description=fake.paragraph(),
    user_id=fake.random_element(User.query.all()).id
  )
  projects.append(project)
db.session.add_all(projects)

# Create some fake iterations
iterations = []
for i in range(10):
  iteration = Iteration(
    name=fake.sentence(),
    description=fake.paragraph(),
    start_date=fake.date_between(start_date='-1y', end_date='today'),
    end_date=fake.date_between(start_date='today', end_date='+1y'),
    project_id=fake.random_element(Project.query.all()).id
  )
  iterations.append(iteration)
db.session.add_all(iterations)

# Create some fake tasks
tasks = []
for i in range(20):
  task = Task(
    title=fake.sentence(),
    description=fake.paragraph(),
    due_date=fake.date_between(start_date='today', end_date='+1y'),
    completed=fake.boolean(),
    user_id=fake.random_element(User.query.all()).id,
    iteration_id=fake.random_element(Iteration.query.all()).id,
    project_id=fake.random_element(Project.query.all()).id
  )
  tasks.append(task)
db.session.add_all(tasks)

# Create some fake tags
tags = []
for i in range(10):
  tag = Tag(
    name=fake.word()
  )
  tags.append(tag)
db.session.add_all(tags)

db.session.commit()
