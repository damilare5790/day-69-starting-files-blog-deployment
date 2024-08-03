# Flask Blog Application

## Table of Contents
- [Flask Blog Application](#flask-blog-application)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Setup and Installation](#setup-and-installation)
  - [Configuration](#configuration)
  - [Database Models](#database-models)
  - [Routes and Views](#routes-and-views)
  - [Forms](#forms)
  - [Authentication and Authorization](#authentication-and-authorization)
  - [Database Migrations](#database-migrations)
  - [Utility Functions](#utility-functions)
  - [Deployment](#deployment)
  - [Contributing](#contributing)

## Introduction

This Flask Blog Application is a full-featured web application that allows users to create, read, update, and delete blog posts. It includes user authentication, commenting system, and an admin interface for managing posts and users.

## Features

- User registration and authentication
- Create, read, update, and delete blog posts
- Commenting system for authenticated users
- Admin-only access for creating and editing posts
- Gravatar integration for user avatars
- CKEditor integration for rich text editing
- Flask-Migrate for database migrations
- Responsive design using Bootstrap 5

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── blog.py
│   ├── forms.py
│   └── utils.py
├── migrations/
├── requirements.txt
├── run.py
├── static/
└── templates/
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/damilare5790/day-69-starting-files-blog-deployment
   cd day-69-starting-files-blog-deployment
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables (see [Configuration](#configuration) section)

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   python run.py
   ```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

```
FLASK_KEY=<your-secret-key>
DB_URI=<your-database-uri>
EMAIL_KEY=<your-email-address>
PASSWORD_KEY=<your-email-password>
```

Make sure to replace the placeholders with your actual values.

## Database Models

The application uses three main models:

1. `User`: Represents registered users
2. `BlogPost`: Represents blog posts
3. `Comment`: Represents comments on blog posts

These models are defined in `app/models.py`.

## Routes and Views

The application's routes are organized into three blueprints:

1. `auth`: Handles user authentication (login, registration, logout)
2. `main`: Handles main pages (home, about, contact)
3. `blog`: Handles blog-related operations (create, read, update, delete posts and comments)

These blueprints are defined in the respective files under `app/routes/`.

## Forms

The application uses WTForms for form handling. The following forms are defined in `app/forms.py`:

- `RegisterForm`: User registration
- `LoginForm`: User login
- `CreatePostForm`: Create or edit blog posts
- `CommentForm`: Add comments to blog posts

## Authentication and Authorization

User authentication is handled using Flask-Login. The `@login_required` decorator is used to protect routes that require authentication.

Two custom decorators are used for authorization:

- `@admin_only`: Restricts access to admin users (user with id 1)
- `@only_commenter`: Allows only the comment author to delete their own comments

These decorators are defined in `app/utils.py`.

## Database Migrations

The application uses Flask-Migrate for database migrations. To create a new migration after changing models:

```
flask db migrate -m "Description of changes"
```

To apply the migration:

```
flask db upgrade
```

## Utility Functions

Utility functions, including the custom decorators and email sending function, are defined in `app/utils.py`.

## Deployment

For deployment:

1. Ensure all environment variables are properly set in your production environment.
2. Run database migrations:
   ```
   flask db upgrade
   ```
3. Use a production WSGI server like Gunicorn:
   ```
   gunicorn run:app
   ```

Consider using a process manager like Supervisor to keep your application running.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request