"""Class CmsiVegtypes holds lists of vegetation types used in CMSi."""

from pandas import Series, DataFrame
import pandas as _pd
from importlib import resources as _resources

import logging as _logging
_logger = _logging.getLogger(__name__)

from . import _data_cmsi
from ..tools import syntaxontools as _syntaxontools

def vegetationtypes(typology='sbbcat', current_only=True, verbose=False):
    """Return list of vegetation type names and codes for given
    typology.
    
    Parameters
    ----------
    typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
        Name of vegetation typology system.

    current_only : boollean, default True
        Return only vegetation types not deprecated.

    verbose : bool, default False
        Show minimal number of columns (False) or all columns (True).

    Returns
    -------
    DataFrame
        
    """
    cst = CmsiSyntaxonTable()
    return cst.vegetationtypes(typology=typology, 
        current_only=current_only, verbose=verbose)


def changes_by_year(typology='sbbcat'):
    """Return table of Creations and Modifications by year for all 
    vegetation types in CMSi.
    
    Parameters
    ----------
    typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
        Code for typology system.

    Returns
    -------
    DataFrame
        Table of changes by year.

    Notes
    -----
    The result shows changes in de list of vegetation types in CMSi. 
    It is not a table of changes in de typology system itself.
        
    """
    cst = CmsiSyntaxonTable()
    return cst.changes_by_year(typology=typology)


class CmsiSyntaxonTable:

    TYPOLOGIES = {
        'VVN Nationale Vegetatie typologie':'vvn',
        'TBO Nationale Vegetatie typologie':'sbbcat',
        'RVVN Nationale Vegetatie typologie':'rvvn',
        }

    SYNTAXON_ORDER = ['klasse', 'orde', 'verbond', 'associatie', 
        'subassociatie', 'klasseromp', 'verbondsromp', 'romp',
        'klassederivaat', 'verbondsderivaat', 'derivaat',
         ]

    COLNAMES_VEGTYPES = [
        'VegClas',
        'GUID',
        'Code',
        'ShortScientificName',
        'LongScientificName',
        'ShortCommonName',
        'LongCommonName',
        'Description',
        'Parent',
        'Quality',
        'IsCurrent',
        'Created',
        'CreatedBy',
        'Modified',
        'ModifiedBy',
        ]

    COLNAMES_RELATIONS = [
        'VegetationTypesGUIDFrom',
        'VegetationTypesGUIDTo',
        'Relation',
        'Priority',
        'VersionNumber',
        'Created',
        'CreatedBy',
        'Modified',
        'ModifiedBy',
        'FROM_GUID',
        'FROM_Code',
        'FROM_ShortScientificName',
        'FROM_LongScientificName',
        'FROM_VegClas',
        'TO_GUID',
        'TO_Code',
        'TO_ShortScientificName',
        'TO_LongScientificName',
        'TO_VegClas',
        ]

    VEGTYPECOLS_MINIMAL = ['Code', 'ShortScientificName', 'ShortCommonName',
        'Created', 'IsCurrent', 'SynLevel', 'SynClass', 'IsLowest',]


    def __init__(self):

        # get table of cmsi vegetation types from package data
        srcfile = (_resources.files(_data_cmsi) / 'CMSiVegetationTypes.csv')
        self._syntaxa = _pd.read_csv(srcfile, encoding='utf-8')

        # convert datetime columns
        for colname in ['Created','Modified']:
            self._syntaxa[colname] = _pd.to_datetime(
                self._syntaxa[colname], format='ISO8601')

        # make field IsCurrent Categoricall
        self._syntaxa['IsCurrent'] = _pd.Categorical(
            values = self._syntaxa['IsCurrent'], 
            categories=['Yes','No'], 
            ordered=True,
            )

        # check for presence of all three typologies
        if not all([(x for x in self._syntaxa['VegClas'].unique()
            if x in self.TYPOLOGIES.keys())]):
                raise inputerror('Unknown typology code in cmsi_vegtypes table.')

        # check for duplicates
        columns = ['VegClas','Code','IsCurrent']
        duplicates = self._syntaxa[self._syntaxa.duplicated(
            subset=columns, keep=False)]
        if not duplicates.empty:
            raise ValueError((f'Vegetation type codes for current '
                f'vegetation types not unique:'
                f'{duplicates.sort_values(by=columns)}'))

        # correct typos
        # -------------
        
        # r43AA01b
        if not self._syntaxa.loc[self._syntaxa['Code']=='r43AA01b',:].empty:
            self._syntaxa.loc[self._syntaxa['Code']=='r43AA01b','Code'] = 'r43Aa01b'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for r43AA01b can be removed.')            

        # 43C1g
        idx = self._syntaxa[self._syntaxa['Code']=='43C1g'].index.values[0]
        if self._syntaxa.loc[idx,'IsCurrent']=='Yes':
            self._syntaxa.loc[idx,'IsCurrent']='No'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for 43C1g can be removed.')            


    def __repr__(self):
        return f'CMSI Vegetationtypes (n={len(self)})'


    def __len__(self):
        return len(self._syntaxa)


    def vegetationtypes(self, typology='sbbcat', current_only=True, verbose=False):
        """Return list of vegetation type names and codes for given
        typology.
        
        Parameters
        ----------
        typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
            Name of vegetation typology system.

        current_only : boollean, default True
            Return only vegetation types not deprecated.

        verbose : bool, default False
            Show minimal number of columns (False) or all columns (True).

        Returns
        -------
        DataFrame
            
        """

        # table of syntaxa for chosen typology
        mask = self._syntaxa['VegClas']==self.typology_longname(typology)
        vegtypes = self._syntaxa[mask].copy()

        # set syntaxcode as index
        vegtypes = vegtypes.set_index('Code', drop=True, 
            verify_integrity=True).sort_index(ascending=True)

        # add columns with syntaxlevel
        vegtypes['SynLevel'] = _pd.Categorical(
            values = vegtypes.index.to_series().apply(
                _syntaxontools.syntaxonlevel, reference=typology),
            categories = self.SYNTAXON_ORDER,
            ordered=True,
            )

        # add column with class number
        vegtypes['SynClass'] = vegtypes.index.to_series().apply(
            _syntaxontools.syntaxonclass)

        # add column indicating if syntaxon is at the lowest level or not
        never_lowest = ['klasse','orde','verbond','nvt']
        idx = vegtypes[vegtypes['SynLevel'].isin(never_lowest)].index.values
        vegtypes.loc[idx,'IsLowest']='No'

        allways_lowest = ['klasseromp','klassederivaat','verbondsromp',
            'verbondsderivaat','subassociatie','romp','derivaat',]
        idx = vegtypes[vegtypes['SynLevel'].isin(allways_lowest)].index.values
        vegtypes.loc[idx,'IsLowest']='Yes'

        # get list of labels for associaties without subassociatie
        # and set lowest to 'Yes'
        mask = vegtypes['SynLevel']=='associatie'
        associaties = vegtypes[mask].index.values

        mask = vegtypes['SynLevel']=='subassociatie'
        associaties_with_sub = vegtypes[mask].index.to_series().str[:-1].unique()

        associaties_without_sub = list(set(associaties)-set(associaties_with_sub))

        vegtypes.loc[associaties_without_sub,'IsLowest'] = 'Yes'
        vegtypes.loc[associaties_with_sub,'IsLowest'] = 'No'

        # make IsLowest categorical column
        vegtypes['IsLowest'] = _pd.Categorical(
            values = vegtypes['IsLowest'],
            categories = ['Yes', 'No'],
            ordered=True,
            )

        if current_only:
            vegtypes = vegtypes[vegtypes['IsCurrent']=='Yes'].copy()

        if not verbose:
            #colnames = [x for x in vegtypes.columns if x in self.VEGTYPECOLS_MINIMAL]
            colnames = [x for x in self.VEGTYPECOLS_MINIMAL if x!='Code']
            vegtypes = vegtypes[colnames].copy()

        # turn date into year
        for colname in ['Created', 'Modified']:
            if colname in list(vegtypes):
                vegtypes[colname] = vegtypes[colname].dt.year.copy()

        return vegtypes

    def typology_longname(self, typology='sbbcat'):
        """Return name of typology for given tyopology code.
        
        Parameters
        ----------
        typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
            Code for typology system.

        Returns
        -------
        str
            Full name of typology
            
        """
        try:
            typology_longname = list(filter(lambda x: self.TYPOLOGIES[x] == typology, 
                self.TYPOLOGIES))[0]
        except IndexError as e:
            raise ValueError((f"Unknown typology code '{typology}'. "
                f"Value must be in {list(self.TYPOLOGIES.values())}."))

        return typology_longname

    def changes_by_year(self, typology='sbbcat'):
        """Return table of Creations and Modifications by year for all 
        vegetation types in CMSi.
        
        Parameters
        ----------
        typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
            Code for typology system.

        Returns
        -------
        DataFrame
            Table of changes by year.
            

        Notes
        -----
        The resul shows changes in de list of vegetation types in CMSi. 
        It is not a table of changes in de typology system itself.
            
        """
        vegtypes = self.vegetationtypes(typology=typology, 
            current_only=False, verbose=True)
        actions = vegtypes[['Created','Modified']].stack().reset_index()
        actions = actions.set_axis(['Code','Action','Year'], axis=1)
        pivot = _pd.pivot_table(data=actions, values='Code', index='Year', 
            columns='Action', aggfunc='count')
        return pivot

