import queue
import logging

DEBUG=True

RADIO_SIGNALS_QUEUE = queue.Queue()

OPERATION_OPTIONS = None

RADIO_ATTEMPS = 3

RADIO_REQUEST = "rpi-rf_send -g 27 -p 332 -t 1 1{table_digits}111"

LOG_PATH = "/var/logs/dcpt.logs" if not DEBUG else "dcpt.logs"