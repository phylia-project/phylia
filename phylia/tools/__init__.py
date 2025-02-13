"""Contains tools for very different purposes:

Functions
---------
year_from_string
    Extract valid year from long strings.
write_to_excel
    Write mulitple pandas dataframes to Excel.


Modules
-------
syntaxtools
    Tools for validating and inspecting syntaxon codes.

filetools
    Tools for handling filepaths.
        
"""

from .conversions import year_from_string
##from ._filetools import relativepath, absolutepath
from . import filetools
##from .sbbprojects import ProjectsTable
from . import syntaxontools
from ._write_excel import write_to_excel
