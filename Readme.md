# VRV_PROJECT

This Flask-based project is designed for user authentication and role management, featuring secure password hashing, token-based authentication using JWT, and Role-Based Access Control (RBAC) for Admin and User roles.

# Setup

Clone the repository to your local machine.
Install the required dependencies using: pip install -r requirements.txt.
Run the application with: python run.py.

# Features

User registration endpoint: /register.
User login endpoint: /login.
Role-protected Admin access: /admin.
Role-protected User access: /user.

# Directory Structure

service.py: Contains application configuration such as database URI and secret keys.
db.py: Defines the database models (User and Role).
main.py: Handles application routing.

# Requirements

Python 3.8 or later.
MySQL database properly configured and running
