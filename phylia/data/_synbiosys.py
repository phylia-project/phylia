"""
Tables from from SynBioSys.
    
"""
import numpy as _np
import pandas as _pd
from importlib import resources as _resources
from . import _synbiosys_data

def rvvn_syntables():
    """Presence and fidelity of species in syntaxa within the rvvn system."""
    srcfile = (_resources.files(_synbiosys_data) / 'synbiosys_syntaxa_tabellen2017.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def rvvn_syntaxa():
    """Return table with list of vegetation types in the revision 
    of the Vegetation of the Netherlands (rVVN)."""
    srcfile = (_resources.files(_synbiosys_data) / 'synbiosys_syntaxa_2017.csv')
    syntaxa = _pd.read_csv(srcfile, encoding='latin-1')
    syntaxa.columns = syntaxa.columns.str.lower()
    return syntaxa.set_index('code').sort_index()


def rvvn_statistics():
    """Return table of desciptive statistics of vegetation types 
    in the revision of the Vegetation of the Netherlands (rVVN)."""
    srcfile = (_resources.files(_synbiosys_data) / 'synbiosys_syntaxa_metadata2017.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def species_2017():
    """Return species list 'soorten_2017'."""
    srcfile = (_resources.files(_synbiosys_data) / 'synbiosys_soorten_2017.csv')
    spec = _pd.read_csv(srcfile, encoding='latin-1')
    spec.columns = map(str.lower,spec.columns)
    spec = spec.set_index('species_nr').sort_index()

    # last column 'fam_nr' in file is float instead of string
    spec['fam_nr'] = spec['fam_nr'].apply(
        lambda x:str(x).split('.')[0] if _pd.notna(x) else _np.nan)

    return spec