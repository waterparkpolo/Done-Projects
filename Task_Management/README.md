Task Management App

A simple task management application built with Flask and SQLite.
It allows users to register, log in, and manage their own private to-do lists.

Features

User registration and login (with password hashing)

Create, view, edit, and delete tasks

Mark tasks as completed

Each user has a private list; no one else can see or modify their tasks

Lightweight frontend using Flask templates (HTML + CSS)

Runs locally with SQLite by default

Requirements

Dependencies are listed in requirements.txt:

Flask==2.2.5
Flask-SQLAlchemy==3.0.3
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

Run the application:

python app.py

Usage

Register a new account at /register

Log in at /login

Manage tasks at /tasks:

Add new tasks with title, description, and due date

Edit or delete existing tasks

Mark tasks as completed

Notes

Passwords are securely hashed with bcrypt (via Passlib).

Data is stored in a local SQLite database (app.db) created automatically.
