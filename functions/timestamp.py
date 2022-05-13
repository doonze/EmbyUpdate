"""
    Returns a timestamp
"""
import time

def time_stamp(print_format: bool = True):
    """
    The time_stamp function returns the current time in a readable format.


    :return: The current date and time in the format mm/dd/yy
    """

    time_now = time.strftime("%x %X", time.localtime())

    if print_format:
        return time_now

    return time_now
