from datetime import datetime
from pytz import timezone
import pytz
from .db.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean

class DataList(Base):
    __tablename__ = 'DataList'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=(0))
    email = Column(String, default=("null"))
    title = Column(String)
    created_date = Column(DateTime, default=(datetime.now(tz=pytz.utc)).astimezone(timezone('US/Pacific')))
    updated_date = Column(DateTime, default=(datetime.now(tz=pytz.utc)).astimezone(timezone('US/Pacific')))
    dev_mode= Column(Boolean, default=(False))
    request= Column(String)
    category= Column(String)
    url= Column(String)
    prompt_response= Column(String)
    return_data= Column(String)
    updated_return_data= Column(String)