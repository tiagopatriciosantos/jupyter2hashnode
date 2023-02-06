"""Top-level package for Jupyter 2 Hashnode."""
from .jupyter2hashnode import Jupyter2Hashnode
from .hashnode import HashnodePoster
import os
import importlib.metadata

_DISTRIBUTION_METADATA = importlib.metadata.metadata('jupyter2hashnode')

__author__ = _DISTRIBUTION_METADATA['Author']
__email__ = _DISTRIBUTION_METADATA['Author-email']
__app_name__ = _DISTRIBUTION_METADATA['Name']
__version__ = _DISTRIBUTION_METADATA['Version']
__homepage__ = _DISTRIBUTION_METADATA['Home-page']


