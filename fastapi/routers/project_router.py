from fastapi import APIRouter, Request, Depends , Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from auth.dependencies import get_current_user
from services import project_service

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/projects")
def project_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    projects = project_service.get_projects_by_user(
        db=db,
        user_id=current_user.id,
    )

    return templates.TemplateResponse(
        request,
        "projects/list.html",
        {
            "current_user":current_user,
            "projects" : projects ,
        }
    )


@router.get("/projects/new")
def project_new(
    request: Request,
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    return templates.TemplateResponse(
        request,
        "projects/new.html",
        {"current_user":current_user}
    )

@router.post("/projects")
def create_project(
     name: str = Form(...),
     description: str = Form(""),
     db : Session = Depends(get_db),
     current_user = Depends(get_current_user)
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    project_service.create_project(
        db=db,
        user_id=current_user.id,
        name=name,
        description=description,
    )

    return RedirectResponse(
        url="/projects",
        status_code=303
    )

@router.get("/projects/{project_id}")
def project_detail(
    project_id : int,
    request : Request,
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303,
        )
    
    project = project_service.get_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id
    )

    return templates.TemplateResponse(
        request,
        "projects/detail.html",
        {
            "current_user": current_user,
            "project" : project,
        }
    )