import argparse

# This sets up the command line arguments
def readArgs(verNum):
    parser = argparse.ArgumentParser(description="An updater for Emby Media Player", prog='EmbyUpdate')
    parser.add_argument('-c', '--config', action='store_true', help='Runs the config updater', required=False)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + verNum,
                        help='Displays version number')
    parser.add_argument('--db_build', action='store_true', help='Builds or rebuilds (Drops/Creates) the database')
    parser.add_argument('-cd', '--config_display', help='Displays all config options. Default: All', nargs='?', const='all')
    args = parser.parse_args()
    return args