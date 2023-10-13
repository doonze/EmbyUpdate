"""
Fix for old version of unzip not being able to create directories. Only used on upgrade from 3.6 to 4.1
"""
import os
import sys
import shutil


def fix_directory():
    """
    This function fixes how the old stupid unzipper in 3.6~ couldn't unzip into directories. When it unzips the new
    4.1+ zip files it just throws everything in to the main directory. Newer versions cannot handle this. So we fix it
    manually. What a pain
    """

    os.chdir(sys.path[0])

    # List of all files that need to be in the functions dir
    functions_list = ['api.py',
                      'arguments.py',
                      'colors.py',
                      'config.py',
                      'configsetup.py',
                      'exceptrace.py',
                      'install.py',
                      'pythonversion.py',
                      'selfupdate.py',
                      'timestamp.py',
                      'updatecheck.py'
                      ]

    # List of all files that need to be in the db dir
    db_list = ['createdb.py',
               'dbfunctions.py',
               'dbobjects.py',
               'editconfig.py'
               ]

    #  List of all files that need to be removed
    remove_list = ['embyupdate.service',
                   'embyupdate.timer',
                   'readme',
                   'configupdate.py'
                   ]

    # If it doesn't exist, create functions dir
    if not os.path.exists('./functions'):
        os.mkdir("functions")

    # If it doesn't exist create db dir
    if not os.path.exists('./db'):
        os.mkdir("db")

    # Copy and then move the init file to the two directories
    if os.path.exists('__init__.py'):
        shutil.copy('__init__.py', './functions/__init__.py')
        shutil.move('__init__.py', './db/__init__.py')

    # Loop through the list and move the files for functions
    for file in functions_list:
        if os.path.exists(f'{file}'):
            shutil.move(f'{file}', f'./functions/{file}')

    # Loop through the list and move the files for db
    for file in db_list:
        if os.path.exists(f'{file}'):
            shutil.move(f'{file}', f'./db/{file}')

    # Loop through the delete list and remove all files we don't want/need
    for file in remove_list:
        if os.path.exists(f'{file}'):
            os.remove(f'{file}')

    # Remove the old beta dir we no longer use
    if os.path.exists('./beta'):
        shutil.rmtree('./beta')
