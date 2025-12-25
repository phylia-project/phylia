
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


def test_taxa():

    df = data.synbiosys.species_2017()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_species_ecology():
    df = data.synbiosys.species_ecology()
    assert isinstance(df, DataFrame)
    assert not df.empty
    
def test_syntaxa_vvn():
    df = data.synbiosys.syntaxa_vvn()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_dbversion():
    res = data.synbiosys.dbversion()
    assert isinstance(res, str)

