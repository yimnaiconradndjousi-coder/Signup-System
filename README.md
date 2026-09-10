# Signup System

A small Flask signup application with a browser frontend, JSON communication, server-side validation, bcrypt password hashing, and SQLite persistence.

![Signup screen](src/signup.png)

## Features

- Signup form served from the frontend
- JSON requests from JavaScript to Flask
- Pydantic validation for username, email, and password
- Additional backend username validation
- Bcrypt password hashing before storage
- SQLite database access through `aiosqlite`
- CORS configuration for local frontend development
- Helpful HTTP responses for successful and invalid requests

## Project Structure

```text
.
├── db/
│   ├── database.py
│   └── userDB.db
├── src/
│   └── signup.png
├── static/
│   ├── main.js
│   └── signup.css
├── templates/
│   └── signup.html
├── main.py
├── schema.py
└── README.md
```

## Requirements

- Python 3.12 or later
- Flask
- Flask-CORS
- Pydantic
- `pydantic[email]`
- bcrypt
- aiosqlite
- Rich

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install Flask[async] flask-cors pydantic[email] bcrypt aiosqlite rich
```

## Run the Backend

From the project directory:

```powershell
python main.py
```

The Flask backend runs at:

```text
http://localhost:8080
```

## Run the Frontend

Serve the project with a local web server such as VS Code Live Server. Open the signup page from the URL provided by that server, commonly:

```text
http://127.0.0.1:5500/templates/signup.html
```

The frontend sends signup data to:

```text
POST http://localhost:8080/signup
```

The backend currently allows these local frontend origins:

- `http://localhost:5500`
- `http://127.0.0.1:5500`

The origin must match the browser URL exactly. `localhost` and `127.0.0.1` are different origins.

## API Example

Request:

```http
POST /signup
Content-Type: application/json
```

```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "a-strong-password"
}
```

Successful response:

```json
{
  "message": "User created successfully"
}
```

The response uses HTTP status `201 Created`.

Invalid data returns HTTP status `400` with an error message.

## Security Notes

- Passwords are hashed with bcrypt before being stored.
- Passwords should never be returned to the frontend or written to logs.
- Backend validation is the security boundary; frontend validation only improves user experience.
- The Flask development server is intended for local development, not production.
- Before deployment, use a production server, HTTPS, secure secret management, rate limiting, and stronger database error handling.
- The SQLite database file is local development data and should not be committed to GitHub.

## Current Status

The signup flow is implemented. Login, sessions, cookies, logout, automated tests, and production deployment are planned next.

## Future Improvements

- Add login and logout endpoints
- Add secure session cookies
- Add duplicate-user error responses such as `409 Conflict`
- Add automated backend and frontend tests
- Improve user-facing success and error messages
- Move documentation images to `docs/images/` if the project grows
