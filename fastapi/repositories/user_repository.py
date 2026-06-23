from sqlalchemy.orm import Session

from models.user import User


def find_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def find_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(
        db: Session,
        username: str,
        password: str,
        display_name: str,
):
    user = User(
        username=username,
        password=password,
        display_name=display_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user