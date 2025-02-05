#Fast API libraries
from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every


#Request model defenitions
from models import TableOrder
from models import TableOrderResponse
from models import TableOrderResponseSuccess
from models import OperationEnum

#Annotation libraries
from pydantic import BaseModel
from typing import Union

#Builting libraries
import requests
import os
import asyncio

#Config file
from settings import *

#Utils
from utils.utils import format_table_number
import time

#Logging
import logging
from logging.handlers import RotatingFileHandler


handler = RotatingFileHandler(
    LOG_PATH,                   # The log file to write to
    maxBytes=5*1024*1024,       # Maximum file size before rotation (5MB in this case)
    backupCount=3               # Keep 3 backup old log files (older ones will be deleted)
)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Create logger and add handler
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)  

def send_signal(radio) -> None:
    for _ in range(RADIO_ATTEMPS):
        logger.info(f"Radio request : {radio}")
        resp = os.popen(radio).read()
        logger.info(f"Radio response : {resp}")


app = FastAPI()


@app.post("/table_order/", 
    status_code=200, 
    response_model=TableOrderResponse,
    responses={
        400: {"model": TableOrderResponse},
        200: {"model": TableOrderResponseSuccess},
        422: {"model": TableOrderResponse},   
    }
)
async def create_item(item: TableOrder, background_tasks: BackgroundTasks) -> JSONResponse:
    """
        The function creates script for radio request and puts it into RADIO_SIGNALS_QUEUE
    """

    code_valid = len(str(item.table)) >= 1 and len(str(item.table)) < 3

    if item.operation not in (OperationEnum.PAID, OperationEnum.ORDER) \
        or item.table is None or not code_valid:
        return JSONResponse(status_code=400, content={"message": "Bad request"})
 
    table_digits = format_table_number(item.operation, item.table)
    radio_request = RADIO_REQUEST.format(table_digits=table_digits)
    background_tasks.add_task(send_signal, radio_request)


    return JSONResponse(status_code=200, content={"message": "Success", "code": table_digits})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)