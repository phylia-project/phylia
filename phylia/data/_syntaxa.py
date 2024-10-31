"""
Module containing functions that return datasets and tables.
    
"""
##import pkg_resources as _pkg_resources
import pandas as _pd
from importlib import resources as _resources

def rvvn_syntables():
    """Presence and fidelity of species in syntaxa within the rvvn system."""

    srcfile = (_resources.files(__package__) / 'synbiosys_syntaxa_tabellen2017.csv')
    #stream = _pkg_resources.resource_stream(__name__,'synbiosys_syntaxa_tabellen2017.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def rvvn_syntaxa():
    """Return table with list of vegetation types in the revision 
    of the Vegetation of the Netherlands (rVVN)."""
    ##stream = _pkg_resources.resource_stream(__name__, 'synbiosys_syntaxa_2017.csv')
    srcfile = (_resources.files(__package__) / 'synbiosys_syntaxa_2017.csv')
    syntaxa = _pd.read_csv(srcfile, encoding='latin-1')
    syntaxa.columns = syntaxa.columns.str.lower()
    syntaxa = syntaxa.set_index('code').sort_index()
    return syntaxa


def rvvn_statistics():
    """Return table of desciptive statistics of vegetation types 
    in the revision of the Vegetation of the Netherlands (rVVN)."""
    #stream = _pkg_resources.resource_stream(__name__,'synbiosys_syntaxa_metadata2017.csv')
    srcfile = (_resources.files(__package__) / 'synbiosys_syntaxa_metadata2017.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def sbbcat_syntaxa():
    """Return table with list of vegetation types in the Staatsbosbeheer
    Catalogus."""
    #stream = _pkg_resources.resource_stream(__name__, 'sbbcat_syntaxonnames.csv')
    srcfile = (_resources.files(__package__) / 'sbbcat_syntaxonnames.csv')
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
    """

    ## This is a stream-like object. If you want the actual info, call
    ## stream.read()
    ##stream = _pkg_resources.resource_stream(__name__, 'beheertypen_kenmerkendheid.csv')
    srcfile = (_resources.files(__package__) / 'beheertypen_kenmerkendheid.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def management_types():
    """Return table with management type codes and names"""
    tbl = sbbcat_characteristic()
    tbl = tbl[['bht_code','bht_naam']].copy()
    tbl = tbl.drop_duplicates().set_index('bht_code').squeeze()
    tbl = tbl.sort_index(ascending=True)
    tbl.name = 'management_types'
    return tbl
