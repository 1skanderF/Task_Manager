from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import engine
from app.models import Base 
from app.routers import auth, users, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/ping")
def ping():
    return {"Success":"True"}

    