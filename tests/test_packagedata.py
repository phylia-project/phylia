
import pytest
from pandas import Series, DataFrame
from phylia import MapData
import phylia.data as data

def test_rvvn():

    df = data.rvvn_syntables()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.rvvn_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.rvvn_statistics()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_sbbcat():

    df = data.sbbcat_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.sbbcat_characteristic()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_management_types():

    sr = data.management_types()
    assert isinstance(sr, Series)
    assert not sr.empty

def test_taxa():

    df = data.species_2017()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_turboveg():

    df = data.tvabund_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.tvhabita_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.tvremarks_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    rec = data.tvabund_fieldtypes()
    assert isinstance(rec, dict)
    assert len(rec.keys())==4
    assert len(rec.values())==4

def test_vegmap():

    mp = data.vegmap_ziewentneede_2022()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    
    mp = data.vegmap_ruinen_1987()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    