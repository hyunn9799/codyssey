from fastapi import APIRouter, Request, Form , Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services import auth_service
from auth.session import login_user, logout_user

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": None}
    )

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db : Session = Depends(get_db),
):
    user = auth_service.authenticate_user(
        db=db,
        username=username,
        password=password,
    )

    if user is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error":"아이디 또는 비밀번호가 올바르지 않습니다."}
        )
    
    login_user(request, user)

    return RedirectResponse(
        url="/projects",
        status_code=303
    )

@router.post("/logout")
def logout(request: Request):
    logout_user(request)

    return RedirectResponse(
        url="/",
        status_code=303
    )