




import pandas as _pd
from importlib import resources as _resources
from . import _vegmap_ZiewentNeede_2022 as _vegmap
from ..sbb._mapdata import MapData

def vegmap_ziewentneede():
    """Return vegetation map data of Ziewent Neede 2022."""
    mdbpath = (_resources.files(_vegmap) / 'Zieuwent_Neede_2022_DS.mdb')
    polypath = (_resources.files(_vegmap) / 'Vlakken_Zieuwent_Neede_2022.shp')
    mapdata = MapData.from_filepaths(mdbpath=mdbpath, polypath=polypath,
        mapname='Ziewent_Neede', mapyear='2022')
    return mapdata
    #mapdata._maptbl._tbldict['SbbType']

