"""
Colors for making pretty
"""
from dataclasses import dataclass
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name

@dataclass
class Terminalcolors:
    '''Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    end =           '\033[0m'
    bold =          '\033[01m'
    disable =       '\033[02m'
    u_line =     '\033[04m'
    reverse =       '\033[07m'
    strikethrough = '\033[09m'
    invisible =     '\033[08m'
    
    class fg:
        black =         '\033[30m'
        red =           '\033[31m'
        green =         '\033[32m'
        orange =        '\033[33m'
        blue =          '\033[34m'
        purple =        '\033[35m'
        cyan =          '\033[36m'
        yellow =        '\033[93m'
        lt_grey =     '\033[37m'
        lt_cyan =     '\033[96m'
        lt_red =      '\033[91m'
        lt_green =    '\033[92m'
        lt_blue =     '\033[94m'
        pink =          '\033[95m'
        dk_grey =      '\033[90m'
        
    class bg:
        black =     '\033[40m'
        red =       '\033[41m'
        green =     '\033[42m'
        orange =    '\033[43m'
        blue =      '\033[44m'
        purple =    '\033[45m'
        cyan =      '\033[46m'
        lightgrey = '\033[47m'