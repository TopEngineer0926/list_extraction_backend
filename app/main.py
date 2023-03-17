from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from .db.database import engine
from app.routers import datalist
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(datalist.router, tags=['Lists'], prefix='/api')

@app.get('/healthchecker')
def root():
    return {'message': 'Hello Moonhub'}