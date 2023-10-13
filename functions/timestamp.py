"""
    Returns a timestamp
"""
import time

def time_stamp(print_format: bool = True):
    """
    The time_stamp function returns the current time in a readable format.


    :return: The current date and time in the format mm/dd/yy
    """

    time_now_print = time.strftime("[%b %d %Y - %r]", time.localtime())
    time_now = time.strftime("%m/%d/%Y %T", time.localtime())

    if print_format:
        return time_now_print

    return time_now
