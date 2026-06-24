from sqlalchemy.orm import Session
from repositories import task_repository

def create_task(
        db:Session, 
        title:str, 
        project_id:int,
        description:str, 
        due_date:str
):
    title = title.strip()

    if not title:
        return None
    
    return task_repository.create_task(
        db = db,
        project_id = project_id,
        title=title,
        description=description,
        due_date=due_date,
    )

def get_tasks(db:Session):
    return task_repository.find_all_task(db)


def get_task_for_user(
    db:Session, 
    task_id:int,
    user_id:int,
):
    return task_repository.find_task_by_id_and_user_id(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

def delete_task(db: Session, task_id: int):
    return task_repository.delete_task(db, task_id)

def update_task(db: Session, task_id: int, title: str, description: str, due_date: str):
    title = title.strip()

    if not title:
        return None

    return task_repository.update_task(
        db=db,
        task_id=task_id,
        title=title,
        description=description,
        due_date=due_date,
    )

def toggle_task_done(db: Session, task_id:int):
    return task_repository.toggle_task_done(db,task_id)

def get_tasks_by_user(db: Session, user_id: int):
    return task_repository.find_tasks_by_user_id(db, user_id)