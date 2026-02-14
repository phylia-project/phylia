

import pytest
from pandas import Series, DataFrame

from phylia.data import sbbweb
import phylia

def test_diagnostic_value():
    sr = sbbweb.diagnostic_value()
    assert isinstance(sr, Series)
    assert not sr.empty

def test_diagnostic_value_definitions():
    df = sbbweb.diagnostic_value_definitions()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_number_of_releves():
    df = sbbweb.number_of_releves()
    assert isinstance(df, Series)
    assert not df.empty

def test_sbb_syntaxa():
    df = sbbweb.sbb_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_species():
    df = sbbweb.species()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_synoptic_tables():
    df = sbbweb.synoptic_tables()
    assert isinstance(df, DataFrame)
    assert not df.empty

