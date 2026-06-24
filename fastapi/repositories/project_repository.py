from sqlalchemy.orm import Session
from models.project import Project

def find_projects_by_user_id(db:Session, user_id:int):
    return (
        db.query(Project)
            .filter(Project.user_id == user_id)
            .order_by(Project.id.desc())
            .all()
    )

def create_project(
        db:Session,
        user_id:int,
        name:str,
        description:str,
):
    project = Project(
        user_id = user_id,
        name = name,
        description = description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project

def find_project_by_id_and_user_id(db: Session, project_id: int, user_id: int):
    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .filter(Project.user_id == user_id)
        .first()
    )

