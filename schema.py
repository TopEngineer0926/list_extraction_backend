from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time, timedelta

class DataList(BaseModel):
    title: str
    request: str
    prompt_response: str
    return_data: str

    class Config:
        orm_mode = True
