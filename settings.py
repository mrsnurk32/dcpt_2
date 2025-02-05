import queue
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


DEBUG = os.getenv("DEBUG") == '1'

RADIO_SIGNALS_QUEUE = queue.Queue()

OPERATION_OPTIONS = None

RADIO_ATTEMPS = 3

RADIO_REQUEST = "rpi-rf_send -g 27 -p 332 -t 1 1{table_digits}111"

LOG_PATH = "/opt/dcpt_2.log" if not DEBUG else "dcpt.logs"