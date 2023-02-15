-- Create a table for users
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL
);

-- Create a table for tasks
CREATE TABLE tasks (
  id INT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  due_date DATE,
  completed BOOLEAN DEFAULT FALSE,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create a table for tags
CREATE TABLE tags (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  color VARCHAR(10) NOT NULL
);

-- Create a table for task_tag relationship
CREATE TABLE task_tag (
  task_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY (task_id, tag_id),
  FOREIGN KEY (task_id) REFERENCES tasks (id),
  FOREIGN KEY (tag_id) REFERENCES tags (id)
);

-- Alter the tasks table and add a new column
ALTER TABLE tasks
ADD completed_at DATETIME;

-- Create a table for projects
CREATE TABLE projects (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create a table for project_task relationship
CREATE TABLE project_task (
  project_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY (project_id, task_id),
  FOREIGN KEY (project_id) REFERENCES projects (id),
  FOREIGN KEY (task_id) REFERENCES tasks (id)
);

-- Create a table for iterations
CREATE TABLE iterations (
  id INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  project_id INT NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects (id)
);

-- Create a table for iteration_task relationship
CREATE TABLE iteration_task (
  iteration_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY (iteration_id, task_id),
  FOREIGN KEY (iteration_id) REFERENCES iterations (id),
  FOREIGN KEY (task_id) REFERENCES tasks (id)
);

