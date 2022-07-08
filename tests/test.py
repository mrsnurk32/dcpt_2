import random
import requests

ALLOWED_TABLES = lambda : random.randint(1, 300)


def test_order_table(attempts = 30):
    method = "/table_order/"
    url = "http://127.0.0.1:8000/table_order/"
    print(url)
    #Testing good requests
    RESPONSES_200 = list()
    for i in range(attempts):
        table = ALLOWED_TABLES()
        resp = requests.post(url, json = {
            "operation":"paid",
            "table": table,
            "waiter": None
        })
        if resp.status_code != 200:
            print(table)
        RESPONSES_200.append(resp.status_code)

    if all([status == 200 for status in RESPONSES_200]):
        print("Success : All the right requests passed")

    else:
        print("Fail : Some requests of good requests have failed")

    # Bad requests
    resp = requests.post(url, json = {
            "operation":None,
            "table": None,
            "waite": None
        })

    if resp.status_code == 200:
        print("Fail : bad request proceed succesfuly")

    else:
        print("Success : bad request did not proceed succesfuly")


    resp = requests.post(url, json = {
        "operation":"paid",
        "table": 123123,
        "waite": None
    })

    if resp.status_code == 200:
        print("Fail : bad request proceed succesfuly")

    else:
        print("Success : bad request did not proceed succesfuly")
    


if __name__ == "__main__":
    test_order_table()