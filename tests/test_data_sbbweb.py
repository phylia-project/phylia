

import pytest
from pandas import Series, DataFrame

from phylia.data import synbiosys_sbbweb
import phylia

def test_diagnostic_value():
    sr = synbiosys_sbbweb.diagnostic_value()
    assert isinstance(sr, Series)
    assert not sr.empty

def test_diagnostic_value_definitions():
    df = synbiosys_sbbweb.diagnostic_value_definitions()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_number_of_releves():
    df = synbiosys_sbbweb.number_of_releves()
    assert isinstance(df, Series)
    assert not df.empty

def test_sbb_syntaxa():
    df = synbiosys_sbbweb.sbb_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_species():
    df = synbiosys_sbbweb.species()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_synoptic_tables():
    df = synbiosys_sbbweb.synoptic_tables()
    assert isinstance(df, DataFrame)
    assert not df.empty

