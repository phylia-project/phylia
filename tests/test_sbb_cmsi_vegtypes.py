
import pytest
from pandas import Series, DataFrame
import pandas as pd
from phylia.data.cmsi import CmsiSyntaxonTable
from phylia.data.cmsi import vegetationtypes


# test class methods
def test_init():
    veg = CmsiSyntaxonTable()
    assert isinstance(str(veg), str)

def test_len():
    veg = CmsiSyntaxonTable()
    assert len(veg.syntaxa)!=0

def test_typology_dict():
    typedict = CmsiSyntaxonTable.TYPOLOGIES
    assert isinstance(typedict, dict)

def test_vegtypes():
    veg = CmsiSyntaxonTable()
    for typology in veg.TYPOLOGIES.values():
        for verbose in [True, False]:
            df = veg.vegetationtypes(typology=typology, verbose=verbose)
            assert isinstance(df, DataFrame)
            assert not df.empty

def test_typology_name():
    veg = CmsiSyntaxonTable()
    for typology in veg.TYPOLOGIES.values():
        name = veg.typology_name(typology=typology)
        assert isinstance(name, str)

def test_changes():
    veg = CmsiSyntaxonTable()
    for typology in veg.TYPOLOGIES.values():
        df = veg.changes_by_year(typology=typology)
        assert isinstance(df, DataFrame)
        assert not df.empty

# test custom functions
def function_cmsi_vegtypes():
    for typology in CmsiSyntaxonTable.TYPOLOGIES.values():
        df = cmsi_vegtypes(typology=typology)
        assert isinstance(df, DataFrame)
        assert not df.empty
