from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, Token
from app.services.user_service import UserService
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    return await UserService.create_user(user)

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    db_user = await UserService.authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}