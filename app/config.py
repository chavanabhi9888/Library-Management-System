from datetime import timedelta

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "library_db"

# JWT settings
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REMEMBER_ME_EXPIRE_DAYS = 7

# File upload directory
BOOKS_DIRECTORY = "uploaded_books/"
