
import pytest
from pandas import Series, DataFrame
from phylia import MapData
import phylia.data.turboveg2 as tvdata


def test_definitions():

    df = tvdata.tvabund_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.tvhabita_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.tvremarks_definition()
    assert isinstance(df, DataFrame)
    assert not df.empty

    rec = tvdata.tvabund_fieldtypes()
    assert isinstance(rec, dict)
    assert len(rec.keys())==4
    assert len(rec.values())==4

def test_floralist():

    df = tvdata.floralist_nederlnd()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.floralist_floranld()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.floralist_floranld_2013()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.floralist_floranld_2017()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.floralist_floranld_2020()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_ecodata():

    df = tvdata.ecodata_nederlnd()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.ecodata_floranld()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.ecodata_floranld_2013()
    assert isinstance(df, DataFrame)
    assert not df.empty
   
    df = tvdata.ecodata_floranld_2017()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tvdata.ecodata_floranld_2020()
    assert isinstance(df, DataFrame)
    assert not df.empty
