

import pytest
from pandas import Series, DataFrame

from phylia.data.cmsi import CmsiSyntaxonTable
from phylia.data import cmsi

import phylia

@pytest.fixture
def typologies():
    return list(CmsiSyntaxonTable.TYPOLOGIES.values())

# test functions
# --------------

def test_fun_changes_by_year(typologies):

    for typology in typologies:
        df = cmsi.changes_by_year(typology=typology)
        assert isinstance(df, DataFrame)
        assert not df.empty

def test_fun_vegetationtypes(typologies):

    for typology in typologies:
        df = cmsi.vegetationtypes(typology=typology, current_only=False, 
            verbose=True)
        assert isinstance(df, DataFrame)
        assert not df.empty

# test class 
# ----------

def test_init():

    cst = CmsiSyntaxonTable()
    df = cst._syntaxa    
    assert isinstance(df, DataFrame)
    assert not df.empty

    assert len(cst)>0

    typedict = CmsiSyntaxonTable.TYPOLOGIES
    assert isinstance(typedict, dict)


def test_typology_longname(typologies):

    cst = CmsiSyntaxonTable()
    for typology in typologies:
        result = cst.typology_longname(typology=typology)
    assert isinstance(typology, str)

    with pytest.raises(ValueError):
        cst.typology_longname(typology='onzin')


def test_changes_by_year(typologies):

    cst = CmsiSyntaxonTable()
    for typology in typologies:
        df = cst.changes_by_year(typology=typology)
        assert isinstance(df, DataFrame)
        assert not df.empty


def test_vegetationtypes(typologies):

    cst = CmsiSyntaxonTable()
    for typology in typologies:
        df = cst.vegetationtypes(typology=typology, current_only=False, verbose=True)
        assert isinstance(df, DataFrame)
        assert not df.empty


