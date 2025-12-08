
import pandas as _pd
from importlib import resources as _resources
from ..io._mapdata import MapData

from ._data_vegmaps import Zieuwent_Neede_2022
from ._data_vegmaps import Ruinen_1987

def zieuwentneede_2022():
    """Return vegetation map data of Ziewent Neede 2022."""
    mdbpath = (_resources.files(Zieuwent_Neede_2022) / 'Zieuwent_Neede_2022_DS.mdb')
    polypath = (_resources.files(Zieuwent_Neede_2022) / 'Vlakken_Zieuwent_Neede_2022.shp')
    mapdata = MapData.from_filepaths(
        mdbpath=mdbpath, 
        polypath=polypath,
        mapname='Ziewent_Neede', 
        mapyear='2022',
        )
    return mapdata

def ruinen_1987():
    """Return vegetation map data of Ziewent Neede 2022."""
    mdbpath = (_resources.files(Ruinen_1987) / '11_Ruinen.mdb')
    polypath = (_resources.files(Ruinen_1987) / 'vlakken.shp')
    mapdata = MapData.from_filepaths(
        mdbpath=mdbpath, 
        polypath=polypath,
        mapname='Ruinen', 
        mapyear='1987',
        )
    return mapdata
