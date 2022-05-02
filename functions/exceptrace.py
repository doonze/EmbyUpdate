import traceback


def execptTrace(string, tracebk):
    type, value, ex_traceback = tracebk
    print(string)
    print()
    for trace in traceback.format_exception(type, value, ex_traceback):
        print(trace)