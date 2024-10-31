
import pandas as _pd
import numpy as _np
from importlib import resources as _resources


def species_2017():

    # link to csv file
    srcfile = (_resources.files(__package__) / 'synbiosys_soorten_2017.csv')

    # read csv with pandas
    spec = _pd.read_csv(srcfile, encoding='latin-1')
    spec.columns = map(str.lower,spec.columns)
    spec = spec.set_index('species_nr').sort_index()

    # last column 'fam_nr' in file is float instead of string
    spec['fam_nr'] = spec['fam_nr'].apply(
        lambda x:str(x).split('.')[0] if _pd.notna(x) else _np.nan)

    return spec

