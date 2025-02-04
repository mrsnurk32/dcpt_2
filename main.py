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
    'app.log',                  # The log file to write to
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
    if item.operation not in (OperationEnum.PAID, OperationEnum.ORDER) \
        or item.table is None or len(str(item.table)) != 2:
        return JSONResponse(status_code=400, content={"message": "Bad request"})
 
    table_digits = format_table_number(item.operation, item.table)
    radio_request = RADIO_REQUEST.format(table_digits=table_digits)
    background_tasks.add_task(send_signal, radio_request)


    return JSONResponse(status_code=200, content={"message": "Success", "code": table_digits})

    
# @app.on_event("startup")
# @repeat_every(seconds=2)
# async def send_signal() -> None:
#     await asyncio.sleep(1)
#     if not RADIO_SIGNALS_QUEUE.empty():
#         elem = RADIO_SIGNALS_QUEUE.get()
#         resp = os.popen(elem).read()


# @app.on_event("startup")
# @repeat_every(seconds=60*3)
# async def get_site() -> None:
#     loop = asyncio.get_event_loop()
#     future = loop.run_in_executor(None, requests.get, 'http://www.google.com')
#     response = await future
#     print(response.status_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)