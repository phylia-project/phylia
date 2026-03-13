"""
Tables developed by Staatsbosbeheer.
"""

from importlib import resources as _resources
import logging as _logging
##from . import _synbiosys_data
import pandas as _pd
from .. import _data_sbb_intern
from ..syntra import TranslateSbbRevision2019

_logger = _logging.getLogger(__name__)


def sbbcat_syntaxa():
    """Return table with list of vegetation types in the Staatsbosbeheer
    Catalogus.
    
    Notes
    -----
    This table has been developed by Piet Schipper.
    
    """
    _logger.warning((f"This method was deprecated. Use 'phylia.data.cmsi.vegetationtypes' instead."))
    return _pd.DataFrame()
    """
    srcfile = (_resources.files(_data_sbb_intern) / 'sbbcat_syntaxonnames.csv')
    sbbcat = _pd.read_csv(srcfile, encoding='latin-1')
    sbbcat = sbbcat.set_index('sbbcat_code').sort_index()

    # remove entries that are not real syntaxa
    mask1 = sbbcat['sbbcat_wetname'].str.startswith('OVERIGE')
    mask2 = sbbcat['sbbcat_wetname'].str.startswith('NVT')
    mask3 = sbbcat['sbbcat_wetname'].str.startswith('VOORLOPIG ONBEKEND')
    return sbbcat[~mask1 & ~mask2 & ~mask3]
    """


def sbbcat_characteristic():
    """Return table with characteristic vegetation types for all
    management types.

    Column kenm contains four classes:
    1 : Very characteristic
    2 : Characteristic
    3 : Less characteristic
    4 : Not characteristic for this management type

    Notes
    -----
    This table has been developed by Piet Schipper.
        
    """
    srcfile = (_resources.files(_data_sbb_intern) / 'beheertypen_kenmerkendheid.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def management_types():
    """Return table with management type codes and names. 

    Notes
    -----
    This table has been developed by Piet Schipper.
           
    """
    tbl = sbbcat_characteristic()
    tbl = tbl[['bht_code','bht_naam']].copy()
    tbl = tbl.drop_duplicates().set_index('bht_code').squeeze()
    tbl = tbl.sort_index(ascending=True)
    tbl.name = 'management_types'
    return tbl


def sbbcat_revision_2019():
    """Return table of translations between SBB Catalogus and the 
    Revision of the Vegetation of the Netherlands.
    
    Notes
    -----
    The table shows translations between syntaxa from the Staatsbosbeheer 
    Catalogus and the Revisie van de Vegetatie van Nederland. Each line 
    shows a unique translation from one type to another.
    Syntaxon codes can appear in multiple rows, as some syntaxa can be 
    translated into multiple syntaxa in the other classification system.
    This table is included here for historical reasons.

    See also the "SbbRevion2019" class for a wrapper around this table 
    with methods for selecting specific data and saving to a formatted Excel
    Workbook.
        
    """
    #srcfile = (_resources.files(_data_sbb_intern) / 'syntaxon_translations_2019.csv')
    #translations = _pd.read_csv(srcfile, encoding='latin-1', dtype='object')
    #translations.index.name = 'translation_id'
    #return translations
    rev = TranslateSbbRevision2019()
    return rev.revisiontable()
    
    
def _sbbcat_diagnostic_species_2014():
    """Return table of diagnstic species for Staatsbosbeheer Catalogus 
    syntaxa. 
    
    Notes
    -----
    The source for this table was a spreadsheet created by Piet Schipper 
    that contained a list of syntaxa and diagnostic species. This 
    spreadsheet was distributed among users of the Staatsbosbeheer 
    Catalogus and when users refer to the Catalogus, they usually mean
    this spreadsheet. The spreadsheet was actively maintained till about 
    2014.
        
    """
    srcfile = (_resources.files(_data_sbb_intern) / 'sbbcatalogus2011_diagnostic_species.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')
