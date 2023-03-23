from fastapi import Depends, HTTPException, status, APIRouter, Body, Response
from sqlalchemy.orm import Session
from typing import Any
from datetime import datetime
from pytz import timezone
import pytz

from .. import crud, schemas, models
from ..db.database import get_db
from .. import task

router = APIRouter()

@router.get('/', response_model= schemas.AllDataListResponse)
def get_datalists(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    datalists = crud.datalist.get_multi(
        db=db, skip=skip, limit=limit
    )
    return {'lists': datalists}


@router.post('/list_text')
def create_datalist(item: schemas.CreateDataListBaseSchema= Body(), db: Session= Depends(get_db)):
    data= task.openai(item.request, item.category)
    info= schemas.CreateDataBaseListBaseSchema(
        title= item.title,
        request= item.request,
        category= item.category,
        url= item.url,
        prompt_response= str(data['prompt_response']),
        return_data= data['return_data']
    )
    print(info)
    new_datalist= models.DataList(**info.dict())
    db.add(new_datalist)
    db.commit()
    db.refresh(new_datalist)
    return {'result': info.return_data, 'id': new_datalist.id}

@router.put('/list_text/{id}', response_model= schemas.UpdateDataListResponse)
def update_datalist(id: str, item: schemas.UpdateDataListSchema= Body(), db: Session= Depends(get_db)):
    datalist_query= db.query(models.DataList).filter(models.DataList.id == id)
    updated_datalist= datalist_query.first()
    now= (datetime.now(tz=pytz.utc)).astimezone(timezone('US/Pacific'))
    temp_return_data= item.return_data
    if (item.dev_mode != True):
        item.return_data= str(item.return_data)
    else:
        item.updated_return_data= str(item.return_data)
        item.return_data= updated_datalist.return_data
    item.updated_date = now
    if not updated_datalist:
        raise HTTPException(status_code= status.HTTP_200_OK,
                            detail= f'No data with this id: {id} found')
    datalist_query.update(item.dict(exclude_unset= True), synchronize_session= False)
    db.commit()
    return {'status': 'success', 'title': updated_datalist.title, 'return_data': temp_return_data}

@router.get('/{id}', response_model= schemas.AllDataListResponse)
def get_datalist(id: str, db: Session = Depends(get_db)):
    list = db.query(models.DataList).filter(models.DataList.id == id).all()
    print(type(list))
    if not list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")
    return {'lists': list}


@router.delete('/{id}')
def delete_datalist(id: str, db: Session = Depends(get_db)):
    datalist_query = db.query(models.DataList).filter(models.DataList.id == id)
    datalist = datalist_query.first()
    if not datalist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')

    datalist_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
