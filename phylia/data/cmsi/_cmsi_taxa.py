
import numpy as _np
from pandas import Series, DataFrame
import pandas as _pd
from importlib import resources as _resources

import logging as _logging
_logger = _logging.getLogger(__name__)

from .. import _data_cmsi

def taxa(include_missing=True, verbose=False):
    taxontable = CmsiTaxonTable()
    taxa = taxontable.taxon_names(
        include_missing=include_missing, 
        verbose=verbose,
        )
    return taxa


class CmsiTaxonTable:
    """Manage tables with taxa from CMSi.""" 

    COLUMN_NAMES = {
        'TaxonName':'taxon_scientificname', 
        'TaxonName2':'taxon_vernacularname',
        'TaxonGroupName':'taxon_group',
        'TaxonRank':'taxon_rank', 
        'ParentTaxon':'taxon_parent',
        }


    def __init__(self):

        # get package data

        srcfile = (_resources.files(_data_cmsi) / 'CMSiPreferredTaxonRegister.csv')
        self._taxon_preferred = _pd.read_csv(srcfile, sep=';', 
            encoding='utf-8', dtype='object')
        #self._taxon_preferred = self._taxon_preferred.set_index(
        #    'PreferredTaxonCode', drop=True, verify_integrity=True)

        srcfile = (_resources.files(_data_cmsi) / 'missing_taxa.xlsx')
        self._missing_taxa = _pd.read_excel(srcfile, dtype='object')

        # synonyms are in seperate list, apparently
        srcfile = (_resources.files(_data_cmsi) / 'CMSiTaxonSynonyms.csv')
        self._taxon_synonyms = _pd.read_csv(srcfile, sep=';', 
            encoding='utf-8', dtype='object')
        #self._taxon_synonyms = self._taxon_synonyms.set_index(
        #    'TaxonCode', drop=True, verify_integrity=True)

        # strangelist: vernacularnames and scientificnames of the same 
        # species have seperate records 
        srcfile = (_resources.files(_data_cmsi) / 'CMSiTaxon.csv')
        self._taxontable = _pd.read_csv(srcfile, sep=';', 
            encoding='utf-8', dtype='object')
        #self._taxontable = self._taxontable.set_index(
        #    'Code', drop=True, verify_integrity=True)



    def __repr__(self):
        return f'{self.__class__.__name__} (n={len(self)})'


    def __len__(self):
        return len(self._taxontable)


    def taxon_names(self, include_missing=True, verbose=False):
        """Return table of taxon names (vascular plants, mosses, lichens 
        and stoneworts only)."""
        taxa = self._taxon_preferred.set_index('TaxonCode', 
            drop=True, verify_integrity=True)

        mask_taxongroup = taxa['TaxonGroupName'].isin(['Vaatplanten','Mossen','Korstmossen','Kranswieren',])
        taxa = taxa[mask_taxongroup].copy()

        if not taxa[taxa.index!=taxa['PreferredTaxonCode']].empty:
            raise ValueError((f"List of taxonnames includes synonyms."))

        if include_missing:
            # add missing species to taxon table
            for idx, row in self._missing_taxa.iterrows():
                if row['TaxonCode'] in taxa.index:
                    raise ValueError((f"Can not insert existing taxon code in taxon list"))
                for col in ['TaxonName','TaxonName2','TaxonGroupName']:
                    taxa.loc[row['TaxonCode'], col]=row[col]

        if not verbose:
            columns = ['TaxonName', 'TaxonName2', 'TaxonGroupName',]
            taxa = taxa[columns].rename(columns=self.COLUMN_NAMES)
            taxa.index.name = 'taxon_code'

        return taxa


    def taxon_groups(self):
        """Return table of taxon groups wityh count of preferred names."""

        taxa = self._taxon_preferred
        taxa = taxa[['TaxonGroupCode','TaxonGroupName']].value_counts().sort_index()        
        return taxa


