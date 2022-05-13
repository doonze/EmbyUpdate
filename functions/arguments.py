"""
command line arguments
"""
import argparse


# This sets up the command line arguments
def read_args(ver_num):
    """
    The read_args function is used to read in the arguments from the command line.
    It returns a list of arguments that can then be passed into other functions.

    Args:
        verNum: Hold the version number of the program

    Returns:
        A dictionary of the arguments passed to it
    """

    parser = argparse.ArgumentParser(
        description="An updater for Emby Media Player", prog='EmbyUpdate')
    parser.add_argument('-c', '--config', action='store_true',
                        help='Runs the config updater', required=False)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + ver_num,
                        help='Displays version number')
    parser.add_argument('--db_build', action='store_true',
                        help='Builds or rebuilds (Drops/Creates) the database')
    parser.add_argument('-cd', '--config_display',
                        help='Displays all config options. Default: All', nargs='?', const='all')
    args = parser.parse_args()
    return args
