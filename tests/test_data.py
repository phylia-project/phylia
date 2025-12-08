
import pytest
from pandas import Series, DataFrame
from phylia import MapData
import phylia.data as data

def test_rvvn():

    df = data.synbiosys.rvvn_syntables()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.synbiosys.rvvn_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.synbiosys.rvvn_statistics()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_sbbcat():

    df = data.sbb.sbbcat_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.sbb.sbbcat_characteristic()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_management_types():

    sr = data.sbb.management_types()
    assert isinstance(sr, Series)
    assert not sr.empty

def test_taxa():

    df = data.synbiosys.species_2017()
    assert isinstance(df, DataFrame)
    assert not df.empty


def test_vegmap():

    mp = data.vegmaps.zieuwentneede_2022()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    
    mp = data.vegmaps.ruinen_1987()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    