"""
Tables from from SynBioSys.
    
"""
import numpy as _np
import pandas as _pd
from importlib import resources as _resources
from . import _data_synbiosys
from ..tools.syntaxontools import syntaxon_validate as _syntaxon_validate

def rvvn_syntables():
    """Presence and fidelity of species in syntaxa within the rvvn system.

    Notes
    -----
    Explanation of columns in this table:

    syncode
        Code of syntaxon in rVVN classification.
    specnr
        Species number in species_2017 species list.
    presence
        Freqeuncy of occurence of the species in the 
        syntaxon in percentage.
    meancov_alll
        Mean cover of the species in all releves,
        including releves where the species is missing.
    meancov_presence
        Mean cover of species in releves where the 
        species is present, calculated as presence*meancov_all.
    fidelity_presence
        Fidelity of the species in the syntaxon based on presence, 
        ignoring cover.
    fidellity_meancover
        Fidelity of the species in the syntaxon based on cover.

    The last two columns are calculated only for syntaxa on the lowest 
    level. This gives an indication for the most probable syntaxon a 
    releve belongs to:

    fidelity_lowest_mip
        Fidelity of species in syntaxon, based on mean cover. 
    fidelity_lowest_presence
        Fidelity of species in syntaxon, based on presence only.
            
    """
    # read file
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_syntaxa_tabellen2017.csv')
    data = _pd.read_csv(srcfile, encoding='latin-1')

    # rename columns
    rename_columns = {
        'SYNTAXON'   : 'syncode',
        'SPECIES_NR' : 'specnr',
        'CONSTANCY'  : 'presence',
        'MEAN'       : 'meancov_all',
        'MEANIFPRES' : 'meancov_presence',
        'PRES_TROUW' : 'fidelity_presence',
        'MEAN_TROUW' : 'fidelity_meancover',
        'FAITHFULNESS_MIP_ALL'  : 'fidelity_lowest_mip',
        'FAITHFULNESS_PRES_ALL' : 'fidelity_lowest_presence',
        }
    data = data.rename(columns=rename_columns)

    # order columns
    colnames = [
        'syncode', 'specnr',
        'presence', 'meancov_all', 'meancov_presence',
        'fidelity_presence', 'fidelity_meancover',
        'fidelity_lowest_mip', 'fidelity_lowest_presence',
        ]
    data = data[colnames].set_index(keys=['syncode','specnr'], verify_integrity=True)
    return data


def rvvn_syntaxa():
    """Return table with list of vegetation types in the revision 
    of the Vegetation of the Netherlands (rVVN)."""
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_syntaxa_2017.csv')
    syntaxa = _pd.read_csv(srcfile, encoding='latin-1')
    syntaxa.columns = syntaxa.columns.str.lower()
    return syntaxa.set_index('code').sort_index()


def rvvn_statistics():
    """Return table of desciptive statistics of vegetation types 
    in the revision of the Vegetation of the Netherlands (rVVN)."""
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_syntaxa_metadata2017.csv')
    return _pd.read_csv(srcfile, encoding='latin-1')


def species_2017():
    """Return species list 'soorten_2017'."""
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_soorten_2017.csv')
    spec = _pd.read_csv(srcfile, encoding='latin-1')
    spec.columns = map(str.lower,spec.columns)
    spec = spec.set_index('species_nr').sort_index()

    # last column 'fam_nr' in file is float instead of string
    spec['fam_nr'] = spec['fam_nr'].apply(
        lambda x:str(x).split('.')[0] if _pd.notna(x) else _np.nan)

    return spec

def species_ecology():
    """Return table of ecological indicator values of species."""
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_soorten_ecodbase.csv')
    ecospec = _pd.read_csv(srcfile, encoding='latin-1', dtype=object, low_memory=False)
    ecospec.columns = map(str.lower,ecospec.columns)
    ecospec.set_index('species_nr', verify_integrity=True)    
    return ecospec


def syntaxa_vvn():
    """Return table of syntaxa in de Vegetatie van Nederland."""
    
    # read source file
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_syntaxa_vvn.csv')
    table = _pd.read_csv(srcfile, encoding='latin-1', dtype=object, low_memory=False)
    table.columns = map(str.lower, table.columns)

    # validate syntaxon codes
    table['code'] = _syntaxon_validate(table['code'])
    #table['parent'] = _syntaxon_validate(table['parent'])

    # reorder columns
    colnames = ['code', 'wetnaam', 'nednaam', 'nednaam_alt', 'isparent', 'hoofdgroep', 'parent']
    newcols = [name for name in colnames if name not in table.columns]
    if newcols:
        raise ValueError((f'Unexpected columns in "synbiosys_syntaxa_vvn": {newcols}'))
    table = table.reindex(columns=colnames)

    # set code as (unique) index
    table = table.set_index('code', verify_integrity=True)

    return table

def dbversion():
    """Return version numbner of SynBioSys database source."""
    # read source file
    srcfile = (_resources.files(_data_synbiosys) / 'synbiosys_dbversion.csv')
    table = _pd.read_csv(srcfile, encoding='latin-1', dtype=object, low_memory=False)
    return table.loc[0, 'version']
