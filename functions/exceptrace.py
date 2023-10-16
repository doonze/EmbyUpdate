"""
module for exception handling
"""
import traceback
from db.dbobjects import Errors
from functions import timestamp as ts


def execpt_trace(string: str, tracebk, process: str):
    """
    The execptTrace function takes a string and traceback object as arguments.
    It prints the string, then for each line in the traceback, it prints:
        - The line number (starting from 1)
        - The file name (the last element of the tuple returned by os.path.split())
        - The function name (the third element of the tuple returned by inspect.getframeinfo())

    Args:
        string: Print the error message
        tracebk: Get the traceback of the exception
        process: Emby or Self
    """

    ex_type, value, ex_traceback = tracebk
    print(string)
    print()
    for trace in traceback.format_exception(ex_type, value, ex_traceback):
        print(trace)
    Errors(date=f'{ts.time_stamp(False)}', message=f'{ex_type} - {value} - {string}', mainorself=process).insert_to_db()
