from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_utils import get_password_hash, verify_password, create_access_token
from app.utils.db_utils import users_collection
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, REMEMBER_ME_EXPIRE_DAYS
from datetime import timedelta
from app.middleware.role_check import require_role
from app.models.user_model import User

router = APIRouter()

@router.post("/users/", dependencies=[Depends(require_role("Admin"))])
def add_user(user: User):
    """Add a new user to the system (Admin only)."""
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    users_collection.insert_one({"username": user.username, "password": hashed_password, "role": user.role})
    return {"message": f"User {user.username} created successfully"}


@router.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    remember_me: bool = Form(False)
):
    user = users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token_data = {"sub": str(user["_id"])}
    expire_time = timedelta(days=REMEMBER_ME_EXPIRE_DAYS) if remember_me else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data=token_data, expires_delta=expire_time)
    
    response = JSONResponse({"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=int(expire_time.total_seconds()),
        samesite="Lax"
    )
    return {"message": "Login successful","token": token}


@router.post("/logout/")
def logout():
    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("access_token")
    return response
