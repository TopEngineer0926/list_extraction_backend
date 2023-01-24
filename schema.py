from pydantic import BaseModel
from typing import Optional

class DataList(BaseModel):
    title: str
    request: Optional[str] = None
    prompt_response: Optional[str] = None    
    return_data: str

    class Config:
        orm_mode = True