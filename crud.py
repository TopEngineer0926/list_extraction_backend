from sqlalchemy.orm import Session
import schema, models


async def get_datalist_info(db: Session, id: int = None):
    if id is None:
        return db.query(models.DataList).all()
    else:
        return db.query(models.DataList).filter(models.DataList.id == id).first()

async def save_datalist_info(db: Session, info: schema.DataList):
    data_listmodel = models.DataList(**info.dict())
    db.add(data_listmodel)
    db.commit()
    db.refresh(data_listmodel)
    return data_listmodel

def update_datalist_info(db: Session, id:int, title:str, list_text: str):
    
    return None

async def delete_datalist(db: Session):
    db.query(models.DataList).delete()

async def error_message(message):
    return {
        'error': message
    }