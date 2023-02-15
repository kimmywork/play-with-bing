
# A RESTful API created by New Bing

## Steps

 - Data modeling (`datamodel.sql`)
   - Create a data model to tracking todo items
   - Create a project model to grouping tasks
   - Create a iteration model to tracking times
 - API
   - Create a rest api to query tasks (`tasks.api`)
   - Implement the api using flask (`app.py`)
   - Rewrite raw db query to SQLAlchemy (end of v1) (`models.py`)
 - RESTful Refactoring
   - Rewrite http api using flask-restful
   - Implement other resources
   - Respond more http verbs (end of v2)
 - Structural refactoring and testing
   - Move resources to different file (`resources.py`)
   - Create mock data (`mock_data.py`)
