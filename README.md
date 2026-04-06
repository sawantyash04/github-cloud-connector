# GitHub Cloud Connector (FastAPI)

A backend project that demonstrates:
- integration with an external API (GitHub REST API)
- secure authentication using a Personal Access Token (PAT)
- usable REST endpoints
- clean, structured, modular code
- error handling and validation

This project was built to satisfy a backend developer assignment that requires a GitHub connector with secure authentication and at least one real GitHub API action.

## Features

### Authentication
- Accepts a GitHub Personal Access Token in the `X-GitHub-Token` request header.
- Supports optional `.env` fallback for local development.
- No hardcoded token in the codebase.

### GitHub API Actions
- Get authenticated GitHub user
- Fetch repositories for a user
- Fetch repositories for an organization
- List issues in a repository
- Create an issue in a repository
- Fetch commits from a repository

### REST Endpoints
- `GET /health`
- `GET /github/me`
- `GET /github/users/{username}/repos`
- `GET /github/orgs/{org}/repos`
- `GET /github/repos/{owner}/{repo}/issues`
- `POST /github/issues`
- `GET /github/repos/{owner}/{repo}/commits`

Alias endpoints for assignment naming:
- `GET /repos/user/{username}`
- `GET /repos/org/{org}`
- `GET /list-issues/{owner}/{repo}`
- `POST /create-issue`

## Project Structure

```text
github_connector_final/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   └── github_client.py
│   └── main.py
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Step-by-Step Setup

### 1) Download and extract the project
Unzip the project folder on your PC.

### 2) Open terminal in the project root
```bash
cd github_connector_final
```

### 3) Create a virtual environment
**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4) Install dependencies
```bash
pip install -r requirements.txt
```

### 5) Run the app
```bash
uvicorn app.main:app --reload
```

Open Swagger UI:
```text
http://127.0.0.1:8000/docs
```

## How to create a GitHub Personal Access Token

1. Sign in to GitHub.
2. Go to **Settings**.
3. Open **Developer settings**.
4. Open **Personal access tokens**.
5. Choose **Fine-grained tokens**.
6. Click **Generate new token**.
7. Give it a name like `github-connector-demo`.
8. Choose the correct owner.
9. Set expiration.
10. Give permissions:
   - **Repository metadata**: Read-only
   - **Issues**: Read and write
11. Generate the token.
12. Copy it immediately and store it safely.

## How authentication works

Pass the token in request header:

```http
X-GitHub-Token: YOUR_GITHUB_PAT
```

You can do this in Swagger UI, Postman, or cURL.

## Example API Calls

### Health check
```bash
curl http://127.0.0.1:8000/health
```

### Get authenticated GitHub user
```bash
curl -X GET "http://127.0.0.1:8000/github/me" \
  -H "X-GitHub-Token: YOUR_TOKEN"
```

### Fetch repositories for a user
```bash
curl -X GET "http://127.0.0.1:8000/github/users/octocat/repos" \
  -H "X-GitHub-Token: YOUR_TOKEN"
```

### Fetch repositories for an organization
```bash
curl -X GET "http://127.0.0.1:8000/github/orgs/github/repos" \
  -H "X-GitHub-Token: YOUR_TOKEN"
```

### List issues from a repository
```bash
curl -X GET "http://127.0.0.1:8000/github/repos/octocat/Hello-World/issues" \
  -H "X-GitHub-Token: YOUR_TOKEN"
```

### Create an issue
```bash
curl -X POST "http://127.0.0.1:8000/github/issues" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Token: YOUR_TOKEN" \
  -d '{
    "owner": "YOUR_USERNAME",
    "repo": "YOUR_REPO",
    "title": "Test issue from connector",
    "body": "Created using my FastAPI GitHub connector"
  }'
```

### Fetch commits
```bash
curl -X GET "http://127.0.0.1:8000/github/repos/octocat/Hello-World/commits" \
  -H "X-GitHub-Token: YOUR_TOKEN"
```

## Run tests
```bash
pytest -q
```

## Upload to your GitHub profile

### 1) Create a new repository on GitHub
Example name:
- `github-cloud-connector`

### 2) Initialize git in the project folder
```bash
git init
git add .
git commit -m "Initial commit: GitHub cloud connector"
```

### 3) Connect your remote repository
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/github-cloud-connector.git
git push -u origin main
```

## Notes
- Never commit your `.env` file.
- Never hardcode your PAT.
- Use Swagger UI for easy demo during interview/submission.
