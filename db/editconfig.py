"""
Used to edit the database configs
"""
from functions.colors import Terminalcolors as c


def edit_config(key_map, dataclass):
    """
    The edit_config function allows the user to edit a specific attribute of a dataclass
    object. The function takes two arguments, key_map and dataclass. Key_map is a dictionary
    that maps line numbers to attributes in the dataclass object that will be edited. Dataclass
    is an instance of one of the classes defined in this module (i.e., Student or Instructor). 
    The function loops until the user enters 'c' or 'C'. If they enter anything else, it checks 
    to see if it's an integer between 1 and len(key_map). If so, then it prompts for new input for 
    the specified attribute.

    Args:
        key_map: Map the user input to a specific attribute of the dataclass
        dataclass: Instantiate the class
    """

    while True:
        print()
        response = input("Enter a line number to edit, or c to cancel: ")
        if response in key_map.keys():
            print()
            update = input(f"The current value is ({c.fg.lt_cyan}"
                           f"{dataclass.__getattribute__(key_map[response])}){c.end}. What "
                           f"would you like to update it to? ")
            dataclass.__setattr__(key_map[response], update)
            dataclass.update_db()
            print()
            print(
                f"{c.fg.lt_cyan}{key_map[response]}{c.end} value has been updated!")
            dataclass.print_me()
            continue

        if response in ("c", "C"):
            return None

        print()
        print(f"{response} {c.fg.lt_red} is Invalid!{c.end} Please try again...")
