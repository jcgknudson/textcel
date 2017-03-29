import logging

from datetime import datetime

def create_window(date_1, date_2, fmt):
    window_begin = datetime.strptime(date_1, fmt) if date_1 else None
    window_end = datetime.strptime(date_2, fmt) if date_2 else None
    #logging.debug(window_begin, window_end)
    window = (window_begin, window_end)
    return window

def create_window(dates, fmt):
    try:
        window_begin = datetime.strptime(dates[0], fmt) if dates[0] else None
        window_end = datetime.strptime(dates[1], fmt) if dates[1] else None
        #logging.debug(window_begin, window_end)
        window = (window_begin, window_end)
    except TypeError as e:
        logging.debug("window is none")
        window = None

    return window
