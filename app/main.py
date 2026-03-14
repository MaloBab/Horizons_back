import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routes import task

from .database import engine
from . import models

from .routes import auth
from .routes import user
from .routes import festival
from .routes import activity
from .routes import tags
from .routes import jobs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Horizons Open Sea Festival",
    description="Backend de gestion des bénévoles et plannings du festival.",
    version="1.0.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY",""),
    https_only=False,  # True en production
)

# Configuration CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(festival.router)
app.include_router(activity.router)
app.include_router(task.router)
app.include_router(tags.router)
app.include_router(jobs.router)