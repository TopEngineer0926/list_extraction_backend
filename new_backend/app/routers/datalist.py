from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Body
from ..database import get_db
from .. import task

router = APIRouter()

@router.get('/', response_model=schemas.DataListResponse)
def get_datalists(db: Session   = Depends(get_db)):
    lists = db.query(models.DataList).group_by(models.DataList.id).all()
    return {'status': 'success', 'results': len(lists), 'posts': lists}

@router.post('/list_text', response_model=schemas.DataListResponse)
def create_datalist(item: schemas.CreateDataListBaseSchema = Body(), db: Session = Depends(get_db)):
    data =task.openai(item.request)
    info = schemas.CreateDataBaseListBaseSchema(
        title= item.title,
        request=item.request,
        prompt_response= str(data['prompt_response']),
        return_data= data['return_data']
    )
    print(info.return_data)
    new_datalist = models.DataList(**info.dict())
    db.add(new_datalist)
    db.commit()
    db.refresh(new_datalist)
    return {'result': info.return_data, 'id':new_datalist.id}

@router.put('/list_text/{id}', response_model=schemas.UpdateDataListResponse)
def update_post(id: str, item: schemas.UpdateDataListSchema = Body(), db: Session = Depends(get_db)):
    print(item)
    datalist_query = db.query(models.DataList).filter(models.DataList.id == id)
    updated_datalist = datalist_query.first()
    print(updated_datalist)
    temp_return_data = item.return_data
    item.return_data = str(item.return_data)
    print(type(item.return_data))
    # return_data = updated_datalist.return_data
    if not updated_datalist:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No data with this id: {id} found')
    datalist_query.update(item.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return {'status': 'success', 'title':updated_datalist.title,'return_data': temp_return_data}

# @router.get('/{id}', response_model=schemas.PostResponse)
# def get_post(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"No post with this id: {id} found")
#     return post


# @router.delete('/{id}')
# def delete_post(id: str, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'No post with this id: {id} found')

#     if str(post.user_id) != user_id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail='You are not allowed to perform this action')
#     post_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
