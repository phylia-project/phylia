
import pytest
from pandas import Series, DataFrame
import pandas as pd
from openpyxl import Workbook

from phylia.data.sbb import sbbcat_syntaxa
from phylia.data.sbb import sbbcat_characteristic
from phylia.data.sbb import management_types
from phylia.data.sbb import sbbcat_revision_2019
from phylia.data.sbb import sbbcat_diagnostic_species_2014
from phylia.data.sbb import sbbcat_diagnostic_species_to_excel
from phylia.data.sbb import SbbDiagnosticSpecies2014
from phylia.data.sbb._sbbdata import _sbbcat_diagnostic_species_2014
from phylia.data.syntra import TranslateSbbRevision2019 # move to seperate test mdule


def test_syntaxa():
    # this method is deprecated
    df = sbbcat_syntaxa()
    assert isinstance(df, DataFrame)
    assert df.empty

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

def test_diagnostic_species_2014():
    df = sbbcat_diagnostic_species_2014()
    assert isinstance(df, DataFrame)
    assert not df.empty

def test_diagnostic_species_to_excel():
    res = sbbcat_diagnostic_species_to_excel()
    assert isinstance(res, Workbook)

def test_class():
    rawtable = _sbbcat_diagnostic_species_2014()
    sbbcat = SbbDiagnosticSpecies2014(rawtable)
    assert isinstance(str(sbbcat), str)
    assert len(sbbcat)!=0
    assert isinstance(sbbcat.syntaxonomic_value_frequency(), pd.DataFrame)
    assert isinstance(sbbcat.syntaxonomic_value_meaning(), pd.DataFrame)
    assert isinstance(sbbcat.to_excel(), Workbook)


def test_revision_2019_class(): # move to new module
    rev = TranslateSbbRevision2019()
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

 
 