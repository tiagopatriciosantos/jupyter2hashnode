"""Top-level package for Jupyter 2 Hashnode."""
import tomli
import importlib.metadata
from .jupyter2hashnode import Jupyter2Hashnode
from .hashnode import HashnodePoster
import os

__author__ = """Tiago Patricio Santos"""
__email__ = 'tiagopatriciosantos@gmail.xcom'
__app_name__ = "jupyter2hashnode"
__version__ = None
try:
    __version__ : importlib.metadata.version('jupyter2hashnode')
except:
    if os.path.exists('pyproject.toml'):
        with open('pyproject.toml', mode='rb') as pyproject:
            __version__ = tomli.load(pyproject)['project']['version']

# if not __version__ :
#     __version__ = "undefined"


 