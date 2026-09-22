from fastapi import Cookie, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import User


def public_user(user):
    return {"id": user.id, "name": user.name, "email": user.email, "phone": user.phone, "address": user.address}


def create_login(user, response):
    response.set_cookie("user_id", str(user.id))
    return public_user(user)


def get_current_user(user_id: int | None = Cookie(default=None), session: Session = Depends(get_session)):
    user = session.get(User, user_id) if user_id else None
    if not user:
        raise HTTPException(401, "Войдите в личный кабинет")
    return user
