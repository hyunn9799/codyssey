from sqlalchemy.orm import Session
from repositories import task_repository

def create_task(db:Session, title:str, description:str, due_date:str):
    title = title.strip()

    if not title:
        return None
    
    return task_repository.create_task(
        db = db,
        title=title,
        description=description,
        due_date=due_date,
    )

def get_tasks(db:Session):
    return task_repository.find_all_task(db)


def get_task(db:Session, task_id:int):
    return task_repository.find_task_by_id(db,task_id)

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