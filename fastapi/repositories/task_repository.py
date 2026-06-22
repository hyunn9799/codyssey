from sqlalchemy.orm import Session
from models.task import Task

def create_task(db:Session , title:str, description:str , due_date: str):
    task = Task(
        title = title,
        description=description,
        due_date=due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def find_all_task(db: Session):
    return db.query(Task).order_by(Task.id.desc()).all()

def find_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    task = find_task_by_id(db, task_id)

    if task is None:
        return False
    
    db.delete(task)
    db.commit()

    return True

def update_task(db:Session, task_id:int, title:str, description: str, due_date: str):
    task = find_task_by_id(db,task_id)

    if task is None:
        return None
    
    task.title = title
    task.description = description
    task.due_date = due_date

    db.commit()
    db.refresh(task)

    return task