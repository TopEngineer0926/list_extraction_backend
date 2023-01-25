from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AllDataListResponse(BaseModel):
    lists: list= []

class DataListResponse(BaseModel):
    id: int
    result: list= []

class ListPostResponse(BaseModel):
    status: str

class UpdateDataListResponse(ListPostResponse):
    title: str
    return_data:list= []

class CreateDataListBaseSchema(BaseModel):
    title: str
    request: str

    class Config:
        orm_mode= True

class CreateDataBaseListBaseSchema(CreateDataListBaseSchema):
    prompt_response: str
    return_data: list= []

    class Config:
        orm_mode= True

class DataListBaseSchema(BaseModel):
    title: str

    class Config:
        orm_mode= True

class UpdateDataListSchema(DataListBaseSchema):
    updated_date: Optional[datetime]= None
    return_data: list= []

    class Config:
        orm_mode= True

class CreateDataListSchema(DataListBaseSchema):
    request: Optional[str]= None
    prompt_response: Optional[str]= None    
    return_data: str

    class Config:
        orm_mode= True