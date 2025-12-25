

import pytest
#from pandas import Series, DataFrame
from phylia import MapData
import phylia.data as data



def test_vegmap():

    mp = data.vegmaps.zieuwentneede_2022()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    
    mp = data.vegmaps.ruinen_1987()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    