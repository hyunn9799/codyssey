from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services import task_service


router = APIRouter()

templates = Jinja2Templates(directory="templates")



@router.get("/tasks")
def task_list(request: Request,
              db:Session = Depends(get_db),
):
    tasks = task_service.get_tasks(db)

    return templates.TemplateResponse(
        request,
        "tasks/list.html",
        {"tasks":tasks}
    )


@router.get("/tasks/new")
def task_new(request:Request):
    return templates.TemplateResponse(
        request,
        "tasks/new.html",
        {}
    )

@router.get("/tasks/{task_id}")
def task_detail(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    task = task_service.get_task(db, task_id)

    return templates.TemplateResponse(
        request,
        "tasks/detail.html",
        {"task":task}
    )

@router.post("/tasks")
def create_task(
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(""),
    db : Session = Depends(get_db),
):
    task_service.create_task(
        db=db,
        title=title,
        description=description,
        due_date=due_date,
    )

    return RedirectResponse(
        url="/tasks",
        status_code=303
    )


@router.post("/tasks/{task_id}/delete")
def delete_task(
    task_id : int,
    db: Session = Depends(get_db),
):
    task_service.delete_task(db, task_id)

    return RedirectResponse(
        url='/tasks',
        status_code=303
    )

@router.get("/tasks/{task_id}/edit")
def task_edit(
    task_id : int,
    request : Request,
    db : Session = Depends(get_db),
):
    task = task_service.get_task(db,task_id)

    return templates.TemplateResponse(
        request,
        "tasks/edit.html",
        {"task":task} 
    )


@router.post("/tasks/{task_id}/edit")
def update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    due_date: str = Form(""),
    db: Session = Depends(get_db),
):
    updated_task = task_service.update_task(
        db=db,
        task_id=task_id,
        title=title,
        description=description,
        due_date=due_date,
    )

    if updated_task is None:
        return RedirectResponse(
            url="/tasks",
            status_code=303
        )
    
    return RedirectResponse(
        url=f"/tasks/{task_id}",
        status_code=303
    )

