from sqlalchemy.orm import Session
from repositories import project_repository

def get_projects_by_user(db:Session, user_id: int):
    return project_repository.find_projects_by_user_id(db,user_id)


def create_project(
        db:Session,
        user_id: int,
        name: str,
        description:str,
):
    name = name.strip()

    if not name:
        return None
    
    return project_repository.create_project(
        db=db,
        user_id=user_id,
        name=name,
        description=description,
    )

def get_project(
        db:Session,
        project_id : int,
        user_id : int,
):
    return project_repository.find_project_by_id_and_user_id(
        db=db,
        project_id=project_id,
        user_id=user_id,
    )