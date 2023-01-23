from datetime import datetime
from pytz import timezone
import pytz
from database import Base
from sqlalchemy import Column, String, Integer, DateTime

class DataList(Base):
    __tablename__ = 'DataList'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    created_date = Column(DateTime, default=(datetime.now(tz=pytz.utc)).astimezone(timezone('US/Pacific')))
    request= Column(String)
    prompt_response= Column(String)
    return_data= Column(String)