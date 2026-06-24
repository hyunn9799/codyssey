from sqlalchemy.orm import Session
from models.task import Task
from models.project import Project

def create_task(
        db:Session , 
        project_id: int,
        title:str, 
        description:str , 
        due_date: str
):
    task = Task(
        project_id = project_id,
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

def find_task_by_id_and_user_id(
        db: Session,
        task_id: int,
        user_id: int,
):
    return (
        db.query(Task)
            .join(Task.project)
            .filter(Task.id == task_id)
            .filter(Project.user_id == user_id)
            .first()
    )

def delete_task(db: Session, task_id: int):
    task = find_task_by_id(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return False
    
    db.delete(task)
    db.commit()

    return True

def update_task(
        db:Session,
        task_id:int,
        title:str, 
        description: str, 
        due_date: str,
):
    task = find_task_by_id(db,task_id)

    if task is None:
        return None
    
    task.title = title
    task.description = description
    task.due_date = due_date

    db.commit()
    db.refresh(task)

    return task

def toggle_task_done(db:Session, task_id:int):
    task = find_task_by_id(db,task_id)

    if task is None:
        return None
    
    task.is_done = not task.is_done

    db.commit()
    db.refresh(task)

    return task


def find_tasks_by_user_id(db: Session, user_id: int):
    return (
        db.query(Task)
            .join(Task.project)
            .filter(Project.user_id == user_id)
            .order_by(Task.id.desc())
            .all()
    )
