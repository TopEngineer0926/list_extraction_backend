from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine
from app.routers import datalist
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(datalist.router, tags=['Lists'], prefix='/api')


@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello Moonhub'}