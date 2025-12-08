"""Phylia is a python package for phytosociological information analyis.
Functionality includes:
- reading Turboveg2 datasets
- reading Standard Turboveg XML files
- reading vegetation map data a used by the National Forestry Institute
  Staatsbosbeheer (using the Digtal Standard data format)
- validating and converting phytosociological syntaxa codes in differtent
  classification systems: Staatsbosbeheer Catalogus, Vegetatie van Nederland 
  and revisie vegetatie van Nederland.
- In the phylia module data several examples of sample data are available.

        
"""
import logging as _logging

from . import io
from . import plots
from . import sampling
from . import tools
from . import data

from ._core._releve import Releve
from .data.cmsi import CmsiSyntaxonTable
from .io._shapefile import ShapeFile
from .io._mdb import Mdb
from .io._tv2db import Tv2Db
from .io._tvxml import TvXml
from .io._maptables import MapTables
from .io._mapelements import MapElements
from .io._mapdata import MapData
from .sampling._samplepolygonmap import SamplePolygonMap
from .plots._sankey_two_maps import SankeyTwoMaps
from .tools.sbbprojects import SbbProjects

_logger = _logging.getLogger(__name__)
#logger.addHandler(logging.NullHandler())
_formatter = _logging.Formatter('%(levelname)s %(message)s')
_console_handler = _logging.StreamHandler()
_console_handler.setLevel(_logging.INFO)  # set log level for console output
_console_handler.setFormatter(_formatter)
_logger.addHandler(_console_handler)