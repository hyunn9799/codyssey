from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine , SessionLocal
from models.task import Task
from models.project import Project
from models.user import User
from routers import home_router, task_router , auth_router
from services.auth_service import create_test_user_if_not_exists

from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="todo-secret-key"
)

Base.metadata.create_all(bind=engine)

def seed_test_user():
    db = SessionLocal()
    try:
        create_test_user_if_not_exists(db)
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home_router.router)
app.include_router(auth_router.router)
app.include_router(task_router.router)


