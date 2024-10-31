
import pytest
from pandas import Series, DataFrame
import phylia

import phylia.data._syntaxa as syntaxa
import phylia.data._taxa as taxa
import phylia.data._turboveg as tv

def test_rvvn():

    df = syntaxa.rvvn_syntables()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = syntaxa.rvvn_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = syntaxa.rvvn_statistics()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_sbbcat():

    df = syntaxa.sbbcat_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = syntaxa.sbbcat_characteristic()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_management_types():

    sr = syntaxa.management_types()
    assert isinstance(sr, Series)
    assert not sr.empty

def test_taxa():

    df = taxa.species_2017()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_turboveg():

    df = tv.tvabund()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tv.tvhabita()
    assert isinstance(df, DataFrame)
    assert not df.empty

    df = tv.tvremarks()
    assert isinstance(df, DataFrame)
    assert not df.empty

    rec = tv.tvabund_types()
    assert isinstance(rec, dict)
    assert len(rec.keys())==4
    assert len(rec.values())==4

