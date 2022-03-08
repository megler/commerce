from datetime import datetime
import time


def datetime_from_utc_to_local(utc_datetime):
    """ Convert UTC to local datetime """

    # Credit: https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp)
    return utc_datetime + offset
