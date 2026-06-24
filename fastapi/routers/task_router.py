from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from database import get_db
from services import task_service, project_service


router = APIRouter()

templates = Jinja2Templates(directory="templates")




@router.get("/tasks/new")
def global_task_new(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    projects = project_service.get_projects_by_user(db, current_user.id)
    if not projects:
        return RedirectResponse(
            url="/projects/new",
            status_code=303
        )
    
    return RedirectResponse(
        url=f"/projects/{projects[0].id}/tasks/new",
        status_code=303
    )


@router.get("/projects/{project_id}/tasks/new")
def task_new(
    project_id : int,
    request: Request,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    project = project_service.get_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    if project is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )

    return templates.TemplateResponse(
        request,
        "tasks/new.html",
        {
            "current_user" : current_user,
            "project" : project,
        }
    )

@router.get("/tasks/{task_id}")
def task_detail(
    task_id: int,
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    task = task_service.get_task_for_user(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )

    return templates.TemplateResponse(
        request, 
        "tasks/detail.html",
        {
            "current_user":current_user,
            "task":task,
        }
    )

@router.post("/projects/{project_id}/tasks")
def create_task(
    project_id : int,
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(""),
    db : Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    project = project_service.get_project(
        db=db,
        project_id=project_id,
        user_id= current_user.id,
    )

    if project is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )

    task_service.create_task(
        db=db,
        project_id=project.id,
        title=title,
        description=description,
        due_date=due_date,
    )

    return RedirectResponse(
        url=f"/projects/{project.id}",
        status_code=303
    )


@router.post("/tasks/{task_id}/delete")
def delete_task(
    task_id : int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    task = task_service.get_task_for_user(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )
    
    project_id = task.project_id

    task_service.delete_task(
        db=db,
        task_id=task.id,
    )

    return RedirectResponse(
        url=f'/projects/{project_id}',
        status_code=303
    )

@router.get("/tasks/{task_id}/edit")
def task_edit(
    task_id : int,
    request : Request,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )


    task = task_service.get_task_for_user(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )

    return templates.TemplateResponse(
        request,
        "tasks/edit.html",
        {
            "current_user":current_user,
            "task":task,
        } 
    )


@router.post("/tasks/{task_id}/edit")
def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(""),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    task = task_service.get_task_for_user(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )

    updated_task = task_service.update_task(
        db=db,
        task_id=task.id,
        title=title,
        description=description,
        due_date=due_date,
    )

    if updated_task is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )
    
    return RedirectResponse(
        url=f"/projects/{updated_task.project_id}",
        status_code=303
    )

@router.post("/tasks/{task_id}/toggle")
def toggle_task_done(
    task_id : int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    if current_user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    task = task_service.get_task_for_user(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        return RedirectResponse(
            url="/projects",
            status_code=303
        )
    
    task_service.toggle_task_done(
        db = db,
        task_id = task.id,
    )
    
    return RedirectResponse(
        url=f"/projects/{task.project_id}",
        status_code=303
    )

