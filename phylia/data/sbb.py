"""
Tables developed by Staatsbosbeheer.
"""

from importlib import resources as _resources
##from . import _synbiosys_data
import pandas as _pd

from . import _data_sbb_intern


def sbbcat_syntaxa():
    """Return table with list of vegetation types in the Staatsbosbeheer
    Catalogus.
    
    Notes
    -----
    This table has been developed by Piet Schipper.
    """
    srcfile = (_resources.files(_data_sbb_intern) / 'sbbcat_syntaxonnames.csv')
    sbbcat = _pd.read_csv(srcfile, encoding='latin-1')
    sbbcat = sbbcat.set_index('sbbcat_code').sort_index()

    # remove entries that are not real syntaxa
    mask1 = sbbcat['sbbcat_wetname'].str.startswith('OVERIGE')
    mask2 = sbbcat['sbbcat_wetname'].str.startswith('NVT')
    mask3 = sbbcat['sbbcat_wetname'].str.startswith('VOORLOPIG ONBEKEND')
    return sbbcat[~mask1 & ~mask2 & ~mask3]

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

