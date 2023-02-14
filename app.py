# Import Flask and Flask-RESTful
from flask import Flask
from flask_restful import Api

# Import the models and resources from models.py and resources.py
from models import db
from resources import TaskResource, SingleTaskResource, UserResource, SingleUserResource, ProjectResource, SingleProjectResource, IterationResource, SingleIterationResource, TagResource, SingleTagResource

# Create the Flask app
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:password@postgres/test'

# Initialize the database with the app
db.init_app(app)

# Create the database tables
@app.before_first_request
def create_tables():
  db.create_all()
  import mock_data
  

# Create the Flask-RESTful API
api = Api(app)

# Register the resources with the API
api.add_resource(TaskResource, '/tasks')
api.add_resource(SingleTaskResource, '/tasks/<int:task_id>')
api.add_resource(UserResource, '/users')
api.add_resource(SingleUserResource, '/users/<int:user_id>')
api.add_resource(ProjectResource, '/projects')
api.add_resource(SingleProjectResource, '/projects/<int:project_id>')
api.add_resource(IterationResource, '/iterations')
api.add_resource(SingleIterationResource, '/iterations/<int:iteration_id>')
api.add_resource(TagResource, '/tags')
api.add_resource(SingleTagResource, '/tags/<int:tag_id>')

# Run the app
if __name__ == '__main__':
  app.run(debug=True)