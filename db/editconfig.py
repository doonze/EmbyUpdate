"""
Used to edit the database configs
"""
from db.dbobjects import DistroConfig
from functions.colors import Terminalcolors as c
from dataclasses import fields


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

def edit_distroconfig(distro_dict):
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
    distroconfig = DistroConfig()
    key_map = {}
    while True:
        print()
        print("Here are the distros you can edit:")
        print()
        for i, key in enumerate(distro_dict.keys(),start=1):
            key_map[str(i)] = key
            print(f"[{c.fg.orange}{i}{c.end}] {c.fg.lt_blue}{key :<16}{c.end}")
                  
        print()
        response = input(f"Enter a distro number to edit it, ({c.fg.orange}a{c.end}) "
                         f"to add one, or ({c.fg.orange}c{c.end}) to cancel: ")

        if response in key_map.keys():
            
            print()
            print(f"{c.fg.yellow}{key_map[response]}:{c.end}")
            distroconfig: DistroConfig = distro_dict[key_map[response]]
            print()
            sub_map = {}
            for i, field in enumerate(fields(distroconfig), start=0):
                if field.name is not ("distro"):
                    sub_map[str(i)] = field.name
                    print(f"[{c.fg.orange}{i}{c.end}] {c.fg.lt_blue}{field.name :<16}{c.end}: "
                        f"{c.fg.lt_cyan}{getattr(distroconfig, field.name)}{c.end}")
            
            print()
            
            response = input(f"Select a number to edit that config item, or ({c.fg.orange}c{c.end}) "
                             f"to cancel: ")
            
            if response in sub_map:
                update = input(f"{c.fg.blue}{sub_map[response]}{c.end}: The current value is "
                       f"({c.fg.lt_cyan}{getattr(distroconfig, sub_map[response])}{c.end}). "
                       f"What would you like to update it to? : ")
            
                distroconfig.__setattr__(sub_map[response], update)
                distroconfig.update_db()
                
                print()
                print(f"{c.fg.lt_cyan}{sub_map[response]}{c.end} value has been updated!")
                
                distroconfig.print_me(single=True)
                
                print()
                response = input("Would you like to update another? [y/N]: ")
                
                if response in ('y', 'Y'):
                    continue
                
                if response in ('n', 'N'):
                    return None
                
        if response in ("c", "C"):
            return None

        print()
        print(f"{response} {c.fg.lt_red} is Invalid!{c.end} Please try again...")