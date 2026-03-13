
import pandas as pd
from openpyxl import Workbook
from phylia.data.syntra import TranslateSbbRevision2019
from phylia.data.syntra import SyntaxonTranslator
from phylia.data.syntra import SbbTranslationsToExcel
from phylia.data.syntra import sbbtranslations_to_excel

def test_revision_2019_class():

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


def test_syntaxontranslatorclass():

    trans = SyntaxonTranslator()

    assert not trans._sbb_to_rvvn().empty
    assert not trans._sbb_back_to_sbb().empty
    assert not trans._rvvn_to_sbb().empty
    assert not trans._rvvn_back_to_rvvn().empty

    assert not trans.syntaxa_sbb().empty
    assert not trans.syntaxa_rvvn().empty
    assert not trans.translation_rules().empty
    assert not trans.crossclasscodes().empty
    assert not trans.translate_sbb_to_rvvn().empty
    assert not trans.translate_rvvn_to_sbb().empty


def test_SbbTranslationsToExcel():
    
    translator = SbbTranslationsToExcel()

    df = translator.rvvn_to_sbb()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    df = translator.sbb_to_rvvn()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    wb = translator.workbook()
    assert isinstance(wb, Workbook)


def test_sbbtranslations_to_excel():

    wb = sbbtranslations_to_excel(lowest_only=False, 
        include_subass=True, fpath=None)
    assert isinstance(wb, Workbook)
    
    #wb = sbbtranslations_to_excel(lowest_only=True, 
    #    include_subass=False, fpath=None)
    #assert isinstance(wb, Workbook)

