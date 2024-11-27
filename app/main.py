from fastapi import FastAPI
from app.routes import auth, admin 

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.on_event("startup")
def startup_event():
    from app.utils.db_utils import users_collection
    from app.utils.auth_utils import get_password_hash

    # Create default users if they don't exist
    if not users_collection.find_one({"username": "admin"}):
        users_collection.insert_one({"username": "admin", "password": get_password_hash("admin123"), "role": "Admin"})
    if not users_collection.find_one({"username": "member"}):
        users_collection.insert_one({"username": "member", "password": get_password_hash("member123"), "role": "Member"})

