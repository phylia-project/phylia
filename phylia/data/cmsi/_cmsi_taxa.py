
import numpy as _np
from pandas import Series, DataFrame
import pandas as _pd
from importlib import resources as _resources

import logging as _logging
_logger = _logging.getLogger(__name__)

from .. import _data_cmsi


class CmsiTaxonTable:
    """Manage tables with taxa from CMSi.""" 

    def __init__(self):

        # get package data
        srcfile = (_resources.files(_data_cmsi) / 'CMSiTaxon.csv')
        self._taxontable = _pd.read_csv(srcfile, sep=';', 
            encoding='utf-8', dtype='object')
        self._taxontable = self._taxontable.set_index(
            'Code', drop=True, verify_integrity=True)

        srcfile = (_resources.files(_data_cmsi) / 'CMSiTaxonSynonyms.csv')
        self._taxon_synonyms = _pd.read_csv(srcfile, sep=';', 
            encoding='utf-8', dtype='object')
        self._taxon_synonyms = self._taxon_synonyms.set_index(
            'TaxonCode', drop=True, verify_integrity=True)

        srcfile = (_resources.files(_data_cmsi) / 'CMSiPreferredTaxonRegister.csv')
        self._taxon_preferred = _pd.read_csv(srcfile, sep=';', 
            encoding='utf-8', dtype='object')
        self._taxon_preferred = self._taxon_preferred.set_index(
            'PreferredTaxonCode', drop=True, verify_integrity=True)


    def __repr__(self):
        return f'{self.__class__.__name__} (n={len(self)})'


    def __len__(self):
        return len(self._taxontable)


    def get_taxon_names(self):
        """Return table of plant names."""
        mask = self._taxon_preferred['TaxonGroupName'].isin(['Vaatplanten','Korstmossen','Mossen','Kranswieren',])
        return self._taxon_preferred[mask]
