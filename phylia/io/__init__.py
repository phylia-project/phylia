"""
Reading data from files.

tools for reading vegetation maps in the data 
format 'Digital Standard' developed around 2004 by Staatsbosbeheer, 
the Dutch National Forestry Service. 

A digtal standard vegetion map comprises an ESRI shapefile with polygons 
(usually called 'vlakken.shp' and a Microsoft Access database with 
information about the content of the polygons. Aditionally a shapefile 
'lijnen.shp' with line elements might be present.

"""

from ._mdb import Mdb
from ._shapefile import ShapeFile
from ._tv2db import Tv2Db
from ._tvxml import TvXml

from ._maptables import MapTables
from ._mapelements import MapElements
from ._mapdata import MapData

