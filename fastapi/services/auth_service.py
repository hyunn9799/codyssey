from sqlalchemy.orm import Session

from repositories import user_repository

TEST_USERNAME = "test"
TEST_PASSWORD = "1234"
TEST_DISPLAY_NAME = "테스트 사용자"

def create_test_user_if_not_exists(db: Session):
    user = user_repository.find_user_by_username(db, TEST_USERNAME)

    if user is not None:
        return user
    
    return user_repository.create_user(
        db=db,
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
        display_name=TEST_DISPLAY_NAME,
    )

def authenticate_user(db:Session, username: str, password: str):
    user = user_repository.find_user_by_username(db, username)

    if user is None:
        return None
    
    if user.password != password:
        return None
    
    return user