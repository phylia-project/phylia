
import pytest
from pandas import Series, DataFrame
from openpyxl import Workbook

from phylia.data.sbb import sbbcat_syntaxa
from phylia.data.sbb import sbbcat_characteristic
from phylia.data.sbb import management_types
from phylia.data.sbb import sbbcat_revision_2019
from phylia.data.sbb import SbbRevision2019

def test_syntaxa():
    df = sbbcat_syntaxa()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_characteristic():
    df = sbbcat_characteristic()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_management_types():
    sr = management_types()
    assert isinstance(sr, Series)
    assert not sr.empty

def test_revision_2019_fun():
    df = sbbcat_revision_2019()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_revision_2019_class():
    rev = SbbRevision2019()
    assert not rev.syntaxa_sbb().empty
    assert not rev.syntaxa_rvvn().empty
    assert not rev.syntaxa_with_multiple_entries().empty
    assert not rev.sbb_syntaxa_not_in_rvvn().empty
    assert not rev.sbb_syntaxa_namechanges().empty
    for from_sys in rev.CLASSIFICATION_COLUMNS.keys():
        for to_sys in rev.CLASSIFICATION_COLUMNS.keys():
            assert not rev.translations().empty
    assert isinstance(rev.revisiontable_to_excel(), Workbook)
    #fpath = r"..\out\sbb_revisie_2019.xlsx"
    #result = rev.revisiontable_to_excel(fpath)


    