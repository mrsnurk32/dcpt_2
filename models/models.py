from pydantic import BaseModel
from typing import Union


class TableOrder(BaseModel):
    operation: Union[str, None] = None
    table: Union[int, None] = None
    waiter: Union[int, None] = None

class TableOrderResponse(BaseModel):
    message : str