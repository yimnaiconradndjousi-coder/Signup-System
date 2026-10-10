# Signup System

A Flask-based signup and authentication app with a browser frontend, async SQLite persistence, and session-based login flow.

## Overview

This project contains a small full-stack authentication system:

- user registration with validation and duplicate checks
- password hashing before storage
- login flow with session cookies
- logout and current-user session checks
- local frontend pages for signup/login
- CORS enabled for local development

The backend uses a Flask app factory and is organized under the `app/` package.

## Features

- Flask app factory with blueprints for auth and registration
- `POST /api/register` for creating accounts
- `POST /api/auth/login` for authenticating users
- `POST /api/auth/logout` for clearing session data
- `POST /api/auth/me` for checking the current logged-in user
- Pydantic request validation for signup and login payloads
- `python_bcrypt` password hashing through the service layer
- SQLite database access using `aiosqlite`
- Session management using Flask cookies
- Local frontend assets served from `static/` and templates in `templates/`

## Project Structure

```text
.
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── schema.py
│   ├── db/
│   │   ├── database.py
│   │   └── userDB.db
│   ├── routes/
│   │   ├── auth.py
│   │   └── register.py
│   └── services/
│       ├── security.py
│       └── users.py
├── src/
│   ├── email2.png
│   ├── facebook.webp
│   ├── ...
│   └── user icon.png
├── static/
│   ├── login.js
│   ├── signup.css
│   └── signup.js
├── templates/
│   ├── login.html
│   ├── signup.html
│   └── index.html
└── .vscode/
```

## Requirements

- Python 3.12+
- Flask
- Flask-CORS
- Pydantic
- python-dotenv
- python_bcrypt
- aiosqlite

These dependencies are listed in `requirements.txt`.

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and set a secret key:

```env
SECRET_KEY=your-secret-key-here
```

## Run the Application

Start the Flask app:

```powershell
python run.py
```

The server runs at:

```text
http://localhost:8080
```

## API Endpoints

### Register a user

```http
POST /api/register
Content-Type: application/json
```

Request body:

```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "a-strong-password"
}
```

Responses:

- `201 Created` with `{ "message": "User created successfully" }`
- `400 Bad Request` for invalid input
- `409 Conflict` when the username or email already exists
- `500 Internal Server Error` for unexpected failures

### Login

```http
POST /api/auth/login
Content-Type: application/json
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "a-strong-password"
}
```

Responses:

- `202 Accepted` with `{ "message": "Login successful" }`
- `400 Bad Request` for invalid credentials or malformed input

### Logout

```http
POST /api/auth/logout
```

Response:

- `200 OK` with `{ "message": "Logged out" }`

### Get current user session

```http
POST /api/auth/me
```

If the user is logged in, the response contains the session user ID:

```json
{
  "id": "<session_id>"
}
```

When no valid session exists, the API returns:

```json
{
  "message": "Authentication required"
}
```

## Frontend Usage

The project includes static HTML pages for signup and login under `templates/`.

Common local frontend URLs when served through a local web server such as VS Code Live Server:

```text
http://127.0.0.1:5500/templates/signup.html
http://127.0.0.1:5500/templates/login.html
```

The frontend JavaScript files in `static/` send requests to the Flask backend on `http://localhost:8080`.

## Security Notes

- Passwords are hashed with bcrypt before being stored.
- Session keys are kept in Flask server-side session storage.
- Backend validation is the primary security layer; browser validation is only a UX improvement.
- The project is intended for local development. For production, use HTTPS, a production WSGI server, and proper secret management.

## Current State

The project is currently implementing a working registration and authentication flow using Flask blueprints and session cookies. The backend routes are active and the frontend pages are wired to the API endpoints.

## Development Notes

- The app is created with `create_app()` in `app/__init__.py`.
- The server is launched from `run.py`.
- The database is stored at `app/db/userDB.db`.
- CORS is configured for local origins, including `http://localhost:5500` and `http://127.0.0.1:5500`.
