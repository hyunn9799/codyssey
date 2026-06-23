from fastapi import Depends,Request
from sqlalchemy.orm import Session

from database import get_db
from repositories import user_repository

from fastapi.responses import RedirectResponse

def get_current_user(
        request:Request,
        db:Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if user_id is None:
        return None
    
    return user_repository.find_user_by_id(db,user_id)

def login_required(
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return None
    
    return current_user