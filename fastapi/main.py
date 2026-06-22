from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from models.task import Task
from routers import home_router, task_router


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home_router.router)
app.include_router(task_router.router)

