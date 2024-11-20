




import pandas as _pd
from importlib import resources as _resources
from ..sbb._mapdata import MapData
from . import _vegmap_ZiewentNeede_2022 as _newvegmap
from . import _vegmap_Ruinen_1987 as _oldvegmap

def vegmap_ziewentneede_2022():
    """Return vegetation map data of Ziewent Neede 2022."""
    mdbpath = (_resources.files(_newvegmap) / 'Zieuwent_Neede_2022_DS.mdb')
    polypath = (_resources.files(_newvegmap) / 'Vlakken_Zieuwent_Neede_2022.shp')
    mapdata = MapData.from_filepaths(
        mdbpath=mdbpath, 
        polypath=polypath,
        mapname='Ziewent_Neede', 
        mapyear='2022',
        )
    return mapdata
    #mapdata._maptbl._tbldict['SbbType']


def vegmap_ruinen_1987():
    """Return vegetation map data of Ziewent Neede 2022."""
    mdbpath = (_resources.files(_oldvegmap) / '11_Ruinen.mdb')
    polypath = (_resources.files(_oldvegmap) / 'vlakken.shp')
    mapdata = MapData.from_filepaths(
        mdbpath=mdbpath, 
        polypath=polypath,
        mapname='Ruinen', 
        mapyear='1987',
        )
    return mapdata
