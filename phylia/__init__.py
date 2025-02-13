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

from . import sbb
from . import read
from . import plot
from . import sample
from . import tools
from . import data

from ._core._releve import Releve
from .sbb._maptables import MapTables
from .sbb._mapelements import MapElements
from .sbb._mapdata import MapData
from .data.cmsi import CmsiSyntaxonTable
from .read._shapefile import ShapeFile
from .read._mdb import Mdb
from .read._tv2db import Tv2Db
from .read._tvxml import TvXml
from .sample._samplepolygonmap import SamplePolygonMap
from .plot._sankey_two_maps import SankeyTwoMaps
from .tools.sbbprojects import SbbProjects

import logging
logger = logging.getLogger(__name__)
#logger.addHandler(logging.NullHandler())

