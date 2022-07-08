#Fast API libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

#Request model defenitions
from models import TableOrder, TableOrderResponse

#Annotation libraries
from pydantic import BaseModel
from typing import Union

#Builting libraries
import requests
import os
import asyncio

#Config file
from settings import *


app = FastAPI()

@app.post("/table_order/", 
    status_code=200, 
    response_model=TableOrderResponse,
    responses={
        400: {"model": TableOrderResponse},
        200: {"model": TableOrderResponse},
        422: {"model": TableOrderResponse},   
    }
)
async def create_item(item: TableOrder) -> JSONResponse:
    """
        The function creates script for radio request and puts it into RADIO_SIGNALS_QUEUE
    """
    if item.operation == SUCCESS_OPERATION and item.table is not None:
        table_number = str(item.table)[::-1]
        table_digits = ["0"] * 3
        if len(table_number) <= len(table_digits):
            for index, value in enumerate([digit for digit in table_number]):
                table_digits[index] = value

            table_digits = ''.join(table_digits[::-1])
            radio_request = RADIO_REQUEST.format(table_digits=table_digits)

            for i in range(RADIO_ATTEMPS):
                RADIO_SIGNALS_QUEUE.put(radio_request)

            return JSONResponse(status_code=200, content={"message": "Success"})

    return JSONResponse(status_code=400, content={"message": "Bad request"})


@app.on_event("startup")
@repeat_every(seconds=2)
async def send_signal() -> None:
    await asyncio.sleep(1)
    if not RADIO_SIGNALS_QUEUE.empty():
        elem = RADIO_SIGNALS_QUEUE.get()
        resp = os.popen(elem).read()


@app.on_event("startup")
@repeat_every(seconds=60*3)
async def get_site() -> None:
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    response = await future
    print(response.status_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)