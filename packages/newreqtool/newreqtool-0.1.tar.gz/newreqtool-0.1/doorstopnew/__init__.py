# SPDX-License-Identifier: LGPL-3.0-only

"""Package for doorstop."""


'''Changes : Commented out some modules which were throwing error 
             and added new import statements  '''


from pkg_resources import DistributionNotFound, get_distribution

from doorstopnew.common import DoorstopError, DoorstopInfo, DoorstopWarning
from doorstopnew.core.document import Document
from doorstopnew.core.item import Item
from doorstopnew.core.tree import Tree
from doorstopnew.core.builder import build
from doorstopnew.core.builder import find_document, find_item
from doorstopnew.core import (
    #document,
    #item,
    #tree,
    #build,
    builder,
    editor,
    exporter,
    #find_document,
    #find_item,
    importer,
    publisher,
)

__project__ = 'Doorstop'

try:
    __version__ = get_distribution(__project__).version
except DistributionNotFound:
    __version__ = '(local)'

CLI = 'doorstop'
GUI = 'doorstop-gui'
SERVER = 'doorstop-server'
VERSION = "{0} v{1}".format(__project__, __version__)
DESCRIPTION = "Requirements management using version control."
