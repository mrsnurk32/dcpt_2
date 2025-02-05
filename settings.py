import queue
import logging

try:
    import dev_settings
    DEBUG = getattr(dev_settings, "DEBUG", False)

except ImportError as err:
    DEBUG = False
    logging.info(f"dev_settings not found: {err}")

except Exception as err:
    DEBUG = False
    logging.error(f"Unexpected error in settings import: {err}")


RADIO_SIGNALS_QUEUE = queue.Queue()

OPERATION_OPTIONS = None

RADIO_ATTEMPS = 3

RADIO_REQUEST = "rpi-rf_send -g 27 -p 332 -t 1 1{table_digits}111"

LOG_PATH = "/var/logs/dcpt.logs" if not DEBUG else "dcpt.logs"