from pydantic import BaseModel
from typing import Union
from enum import Enum


class OperationEnum(str, Enum):
    PAID = "paid"
    ORDER = "order"


class TableOrder(BaseModel):
    operation: Union[OperationEnum, None] = None
    table: Union[int, None] = None
    waiter: Union[int, None] = None

class TableOrderResponse(BaseModel):
    message : str


class TableOrderResponseSuccess(BaseModel):
    message : str
    code: str