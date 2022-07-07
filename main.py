from typing import Union
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

import os
import time

OPERATION_OPTIONS = None

SUCCESS_OPERATION = 'paid'

RADIO_ATTEMPS = 3

RADIO_REQUEST = "rpi-rf_send -g 27 -p 332 -t 1 1{table_digits}111"

class TableOrder(BaseModel):
    operation: Union[str, None] = None
    table: Union[int, None] = None
    waiter: Union[int, None] = None

app = FastAPI()

@app.post("/table_order/", status_code=200)
async def create_item(item: TableOrder):
    context = {
        "status": "Failure"
    }
    if item.operation == SUCCESS_OPERATION and item.table is not None:
        table_number = str(item.table)[::-1]
        table_digits = ["0"] * 3
        if len(table_number) <= len(table_digits):
            for index, value in enumerate([digit for digit in table_number]):
                print(index, value)
                table_digits[index] = value

            table_digits = ''.join(table_digits[::-1])
            radio_request = RADIO_REQUEST.format(table_digits=table_digits)

            for i in range(RADIO_ATTEMPS):
                resp = os.popen(radio_request).read()
                time.sleep(1)

            context["status"] = "Success"
            return context

    # response.status_code = status.HTTP_201_CREATED
    return context

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)