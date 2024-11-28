
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

def test_turboveg():

    df = data.turboveg2.tvabund_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.turboveg2.tvhabita_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = data.turboveg2.tvremarks_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    rec = data.turboveg2.tvabund_fieldtypes()
    assert isinstance(rec, dict)
    assert len(rec.keys())==4
    assert len(rec.values())==4

def test_vegmap():

    mp = data.vegmaps.zieuwentneede_2022()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    
    mp = data.vegmaps.ruinen_1987()
    assert isinstance(mp, MapData)
    assert not mp.maptables.empty
    assert not mp.polygons.empty
    