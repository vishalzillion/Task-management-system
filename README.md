# Task-management-system

This is a GraphQL API built using Graphene Django for a task management application. 

## Features

- User authentication using GraphQL JWT
- Manage tasks assigned to users
- Categorize tasks into different buckets
- Track task progress and completion
- Search and filter tasks by title, description etc
- Generate weekly analytics for tasks
- Granular permissions for mutations

## Models

The main models are:

- **User** - Stores user accounts 
- **Task** - Represents tasks assigned to users
- **Category** - Categories for grouping different tasks
  
## Schema and Queries

The main queries implemented are:

- `allTasks` - Get list of tasks
- `searchTasks` - Search tasks by title or description
- `weeklyStats` - Get analytics for tasks in a date range

Some of the mutations are:

- `createUser` - Create a new user account
- `createTask` - Create a new task 
- `markTaskCompleted` - Mark a task as completed

## Local Development

### Dependencies

- Python 3.6+
- Django 2.2+
- Graphene Django 2.0+

### Running locally

- Clone the repository using "git clone 'repository url' "
- Install dependencies `pip install requirements.txt`
- Run migrations `python manage.py migrate`
- Start development server `python manage.py runserver`
- Access GraphiQL at `http://127.0.0.1:8000/graphql`

