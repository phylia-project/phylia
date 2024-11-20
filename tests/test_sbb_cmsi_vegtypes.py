
import pytest
from pandas import Series, DataFrame
import pandas as pd
from phylia.sbb import CmsiVegtypes
from phylia.sbb import cmsi_vegtypes


# test class methods
def test_init():
    veg = CmsiVegtypes()
    assert isinstance(str(veg), str)

def test_len():
    veg = CmsiVegtypes()
    assert len(veg._cmsi_vegtypes)!=0

def test_typology_dict():
    typedict = CmsiVegtypes.TYPOLOGIES
    assert isinstance(typedict, dict)

def test_vegtypes():
    veg = CmsiVegtypes()
    for typology in veg.TYPOLOGIES.values():
        for verbose in [True, False]:
            df = veg.vegetation_types(typology=typology, verbose=verbose)
            assert isinstance(df, DataFrame)
            assert not df.empty

def test_typology_name():
    veg = CmsiVegtypes()
    for typology in veg.TYPOLOGIES.values():
        name = veg.get_typology_name(typology=typology)
        assert isinstance(name, str)

# test custom functions
def function_cmsi_vegtypes():
    for typology in CmsiVegtypes.TYPOLOGIES.values():
        df = cmsi_vegtypes(typology=typology)
        assert isinstance(df, DataFrame)
        assert not df.empty
