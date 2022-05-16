"""
Python version Check
"""
import sys
from functions.colors import Terminalcolors as c
def python_version_check():
    """
    The python_version_check function checks the version of Python being used to run this script.
    Python 3.6+ is required for use of this program, and if a version below that is used, the
    program will exit.

    :return: The version of python you are running
    """
    python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1])
    if int(sys.version_info[0]) < 3:
        print("")
        print("You are running Python version " + python_version + " Python 3.6+ is required! "
              "Exiting!!")
        sys.exit()

    if (sys.version_info[0] == 3 and int(sys.version_info[1]) < 6):
        print()
        print("You are running Python version " + python_version + " Python 3.6+ is "
              "required! Exiting!!")
        sys.exit()

    print()
    print(f"You are running Python version {python_version} ,{c.fg.green}CHECK PASSED{c.end}!")
    