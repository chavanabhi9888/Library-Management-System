# FastAPI Project

This project is a backend application built using **FastAPI**, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.

---

## Features

- User authentication with roles (Admin, Member)
- Cookie-based authentication with "Remember Me" functionality
- RESTful APIs for managing books
- File upload support
- Modular and scalable project structure
- Secure password hashing and token-based authentication
- Integration with MongoDB for database management

---

## Prerequisites

- Python 3.7 or higher
- MongoDB (running locally or hosted)
- Recommended: `virtualenv` for managing virtual environments

---

## Installation

1. **Clone the repository**:
   git clone https://github.com/Library-Management-System/
   cd Library-Management-System

2 **Create and activate a virtual environment:**

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies:**

pip install -r requirements.txt
Set up environment variables: Create a .env file at the root of the project and add the following:

4. **Add your credential config.py**
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REMEMBER_ME_EXPIRE_DAYS=7
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=fastapi_db
BOOKS_DIRECTORY=./uploaded_files

5. **Run the application:**

uvicorn app.main:app --reload
