"""Contains tools for very different purposes:

Functions
---------
absolutepath
    Transform relative path to absolute path.
relativepath
    Transform absolute path tot relative ppath.
year_from_string
    Extract valid year from long strings.
write_to_excel
    Write mulitple pandas dataframes to Excel.


Modules
-------
syntaxtools
    Tools for validating and inspecting syntaxon codes.
        
"""

from ._conversions import year_from_string
from ._filetools import relativepath, absolutepath
from ._projectstable import ProjectsTable
from . import syntaxontools
from ._write_excel import write_to_excel
