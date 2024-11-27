from fastapi import HTTPException, Depends, Request
from app.utils.auth_utils import decode_access_token
from app.utils.db_utils import users_collection
from bson import ObjectId

def get_current_user(request: Request):
    # token = request.cookies.get("access_token")  # Fetch token from cookies
    token = request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_access_token(token.split(" ")[1])
    user = users_collection.find_one({"_id": ObjectId(payload.get("sub"))})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



def require_role(*roles: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden, You don't have access")
        return user
    return role_checker
