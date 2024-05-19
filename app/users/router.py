from fastapi import APIRouter, Depends, Response, status

from app.exceptions import UserAlreadyExistsException
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth & Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: SUserAuth) -> None:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.hashed_password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(user_data: SUserAuth, response: Response) -> dict:
    user = await authenticate_user(user_data.email, user_data.hashed_password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"message": "successful login"}


@router.post("/logout")
async def logout_user(response: Response) -> dict:
    response.delete_cookie("booking_access_token")
    return {"message": "successful logout"}


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
