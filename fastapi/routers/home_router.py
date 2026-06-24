from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from auth.dependencies import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(
    request: Request,
    current_user = Depends(get_current_user)
):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "app_name": "나의 할 일 앱",
            "current_user": current_user,
        }
    )