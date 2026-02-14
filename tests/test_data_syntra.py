

from openpyxl import Workbook
from phylia.data.syntra import TranslateSbbRevision2019


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

