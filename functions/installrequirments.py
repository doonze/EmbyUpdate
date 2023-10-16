"""
module for installing requirements
"""
import importlib
import importlib.metadata
import subprocess
import sys


def install_req():
    packages = ['requests']
    [subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
     for pkg in packages if not importlib.metadata.distribution(pkg)]
    print("done")
