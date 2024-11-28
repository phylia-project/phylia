"""
Tables behind the webapplication
https://www.synbiosys.alterra.nl/sbbcatalogus/

They contain syntoptic tables for the Staatsbosbeheer Catalogus,
and diagnostic value of species.
        
"""

from pandas import Series, DataFrame
import pandas as _pd
from importlib import resources as _resources

from . import _data_synbiosys_sbbweb

def sbb_syntaxa():
    """Return list of valid syntaxa in the Staatsbosbeheer Catalog."""
    srcfile = (_resources.files(_data_synbiosys_sbbweb) / 'sbbtypen.csv')
    data = _pd.read_csv(srcfile, encoding='utf-8')
    return data.set_index('syntaxon', verify_integrity=True)

def species():
    """Return list of valid species names."""
    srcfile = (_resources.files(_data_synbiosys_sbbweb) / 'soortenlijst.csv')
    data = _pd.read_csv(srcfile, encoding='utf-8')
    return data.set_index('species_nr', verify_integrity=True)

def diagnostic_value():
    """Diagnostic value for species in SBB syntaxa."""
    srcfile = (_resources.files(_data_synbiosys_sbbweb) / 'status_soorten_data.csv')
    data = _pd.read_csv(srcfile, encoding='utf-8')
    data = data.set_index(['species_nr','syntaxon'], 
        verify_integrity=True).squeeze()
    data.name = 'diagnostic_value'
    return data

def diagnostic_value_definitions():
    """Definitions of diagnostic value status for species in SBB syntaxa."""
    srcfile = (_resources.files(_data_synbiosys_sbbweb) / 'status_soorten.csv')
    data = _pd.read_csv(srcfile, encoding='utf-8')
    data = data.set_index('code').sort_values('volgorde', ascending=False)
    return data[['omschrijving','volgorde']]

def synoptic_tables():
    """Synoptic tables for the Staatsbosbeheer Catalog."""
    srcfile = (_resources.files(_data_synbiosys_sbbweb) / 'synoptab.csv')
    data = _pd.read_csv(srcfile, encoding='utf-8')
    return data.set_index(['species_nr','syntaxon'], verify_integrity=True)

def number_of_releves():
    """Return list with number of typical releves for each syntaxon in 
    the Staatsbosbeheer Catalog."""
    srcfile = (_resources.files(_data_synbiosys_sbbweb) / 'metadata.csv')
    data = _pd.read_csv(srcfile, encoding='utf-8')
    return data.set_index('syntaxon', verify_integrity=True).squeeze()
