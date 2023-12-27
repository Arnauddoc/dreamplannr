# Online Planner

Welcome to the Online Planner project! This web application allows users to manage their tasks, store to-do lists, and maintain an agenda. 
It comes with authentication features to ensure secure access to user-specific data.

## Features

- **Task Management:** Create, update, and delete tasks to stay organized.
- **To-Do Lists:** Maintain to-do lists to keep track of pending items.
- **Agenda:** Plan and schedule events with the built-in agenda.
- **User Authentication:** Securely manage your tasks with user authentication.
- **Database Connectivity:** Utilizes a database to store and retrieve task data.

## Requirements

Ensure you have the following requirements installed to run the project:

- Python 3.x
- Django 3.x
- MySQL or another compatible database system
- Additional Python packages:
  whitenoise
  crispy_forms
  
-Create a virtual environment:
  python -m venv venv
-Activate the virtual environment
-pip install -r requirements.txtSet up the database:

Update the DATABASES configuration in settings.py to connect to your database.

-Apply migrations:
  python manage.py migrate
-Create a superuser account:
  python manage.py createsuperuser

Run the development server:
  python manage.py runserver

Result!!
  https://docdc.pythonanywhere.com/
