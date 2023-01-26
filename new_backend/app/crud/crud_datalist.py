from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import DataList
from app.schemas import CreateDataListBaseSchema, UpdateDataListSchema


class CRUDItem(CRUDBase[DataList, CreateDataListBaseSchema, UpdateDataListSchema]):
    def create(
        self, db: Session, *, obj_in: CreateDataListBaseSchema
    ) -> DataList:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

datalist = CRUDItem(DataList)
