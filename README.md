# Users API

![User page](/users.png)

A small JSON API for creating, listing, searching, and retrieving users with Flask and MySQL.
## Setup

Requirements: Python 3.11 and a running MySQL Server. The home page at `/` is an interactive interface; the `/users` endpoints remain JSON APIs.

1. Start MySQL Server. On Windows, open the Start menu, search for **Services**, and start the installed MySQL service (often named `MySQL80`). You can check its status in PowerShell with:

	```bash
Get-Service *mysql*
	```

2. From the project folder, create the database and table. The command prompts for the MySQL root password:

	```bash
Get-Content .\schema.sql | mysql -u root -p
	```

	If `mysql` is not recognized, add the MySQL `bin` folder to your PATH or run `mysql.exe` using its full installation path.

3. Create and activate a virtual environment, then install dependencies:

	```powershell
	py -m venv .venv
	.venv\Scripts\Activate.ps1
	pip install -r requirements.txt
	```

	On macOS or Linux, activate it with `source .venv/bin/activate`.

4. Set the MySQL connection string to match your MySQL username and password. For example, in PowerShell:

	```powershell
	$env:DATABASE_URL = "mysql+pymysql://root:your-password@localhost/users"
	```

5. Start Flask:

	```sh
	flask --app app run --debug
	```

	Open `http://127.0.0.1:5000` for the interactive page. The JSON API is available at `http://127.0.0.1:5000/users`.

## Endpoints

All responses are JSON. User objects contain `id`, `name`, `email`, and `role`.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/users` | List users; accepts `search`, `page`, and `limit` query parameters |
| `POST` | `/users` | Create a user |
| `GET` | `/users/<id>` | Retrieve one user |

List or search users:

```sh
curl "http://127.0.0.1:5000/users?search=Rahul&page=1&limit=10"
```

```json
{
  "success": true,
  "data": [{ "id": 1, "name": "Rahul Verma", "email": "rahul@gmail.com", "role": "engineer" }],
  "page": 1,
  "limit": 10,
  "total": 1
}
```

Create a user:

```sh
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul Verma","email":"rahul@gmail.com","role":"engineer"}'
```

```json
{
  "success": true,
  "data": { "id": 1, "name": "Rahul Verma", "email": "rahul@gmail.com", "role": "engineer" }
}
```

Retrieve one user with `GET /users/1`; the response uses the same `data` object. Errors use this shape:

```json
{ "success": false, "error": "User not found" }
```

Missing/invalid fields and invalid pagination return `400`; duplicate email returns `409`; a missing user returns `404`.

## Database

`schema.sql` creates the `users` database and a `users` table with an auto-increment integer primary key, required `name`, unique required `email`, and required `role`.

## Assumptions

- Email uniqueness is case-sensitive or case-insensitive according to the MySQL column collation in use.
- Search is a partial, case-insensitive match against name or email.
- Pagination defaults to page 1 with 10 results; page and limit must be positive integers, and limit is capped at 100.
- Authentication and user updates/deletes are outside the requested scope.

## Short Answers

1. **Why Flask?** 
 It is lightweight and makes the request, validation, and database flow easy to follow for this small API.

2. **How would you scale it?** 
	- Use connection pooling to reuse existing database connections.
	- Using a MySQL service with indexes and add caching (like Redis) and monitoring where measurements show they are needed.
	- Using modular structure to make changes easier and document each features.

3. **Production changes?** 
	- Disable debug mode, load secrets from a secret manager for environment file data
	- Adding authentication and authorization 
	- Structured logs, automated tests, rate limiting, then deploy behind HTTPS.

## AI Usage Declaration

- **AI tool used:** GitHub Copilot.
- **AI-generated:** The initial Flask application structure, template UI and documentation were created with AI assistance.
- **Manual modifications:** 
	- MySQL connection was made
	- Environment variable setup, gitignore.
	- Integrated template for UI part to interact.
	- 
	