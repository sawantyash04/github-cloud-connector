# 🚀 GitHub Cloud Connector (FastAPI)

A production-ready backend service that integrates with the GitHub REST API to perform real-world actions such as fetching repositories, listing issues, creating issues, and retrieving commits.

This project demonstrates strong backend engineering fundamentals including secure authentication, external API integration, clean architecture, and robust error handling.

---

## ✨ Key Highlights

- 🔐 Secure authentication using GitHub Personal Access Token (PAT)
- 🔗 Real-time integration with GitHub REST API
- ⚡ FastAPI-based RESTful service with interactive Swagger UI
- 🧩 Modular architecture (routes, services, schemas, config)
- ❗ Comprehensive error handling (401, 403, 404, 422, 500)
- 🧪 Unit-tested endpoints

---

## 🛠 Tech Stack

- **Backend:** Python
- **Framework:** FastAPI
- **HTTP Client:** HTTPX
- **Validation:** Pydantic
- **Testing:** Pytest

## Project Structure 

github_connector/
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
│   ├── utils/
│   │   └── mappers.py
│   └── main.py
├── tests/
├── .env.example
├── README.md
└── requirements.txt

## How to run the Project 

Step 1 : Download and extract

Download Yash_Sawant_Backend_Assignment.zip and extract it.

Step 2 : Open terminal in the project folder
cd github_connector_final

Step 3 : Create virtual environment
python -m venv venv

Step 4 : Activate virtual environment
venv\Scripts\activate

Step 5 : Install dependencies
pip install -r requirements.txt

Step 6 : Start the server
uvicorn app.main:app --reload

Step 7 : Open Swagger UI
Open this in browser:
http://127.0.0.1:8000/docs

Step 8 : How Authentication Works 
Pass your GitHub Personal Access Token in request header:

X-GitHub-Token: "YOUR_GITHUB_PAT"
