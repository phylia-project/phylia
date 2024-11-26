"""Class CmsiVegtypes holds lists of vegetation types used in CMSi."""

from pandas import Series, DataFrame
import pandas as _pd

from . import _data_cmsi

def cmsi_vegtypes(typology='sbb'):
    """Return table of vegetation types used in CMSi.
    
    Parameters
    ----------
    typology : {'sbb','rvvn','vvn'}, default 'sbb'
        Reference typology system.

    Returns
    -------
    DataFrame
        Table of vegetation types for chosen reference system.
        
    """
    cmsi = CmsiVegtypes()
    return cmsi.vegetation_types(typology=typology)


class CmsiVegtypes:

    TYPOLOGIES = {
        'VVN Nationale Vegetatie typologie':'vvn',
        'TBO Nationale Vegetatie typologie':'sbb',
        'RVVN Nationale Vegetatie typologie':'rvvn',
        }

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
        'Created']


    def __init__(self):

        # get table of cmsi vegetation types from package data
        srcfile = (_resources.files(_data_cmsi) / 'CMSiVegetationTypes.csv')
        return _pd.read_csv(srcfile, encoding='utf-8') #latin-1')


        # convert datetime columns
        for colname in ['Created','Modified']:
            self._cmsi_vegtypes[colname] = _ .to_datetime(
                self._cmsi_vegtypes[colname], format='ISO8601')

        # check for presence of all three typologies
        if not all([(x for x in self._cmsi_vegtypes['VegClas'].unique() 
            if x in self.TYPOLOGIES.keys())]):
                raise inputerror('Unknown typology code in cmsi_vegtypes table.')

        # check for duplicates
        columns = ['VegClas','Code','IsCurrent']
        duplicates = self._cmsi_vegtypes[self._cmsi_vegtypes.duplicated(
            subset=columns, keep=False)]
        if not duplicates.empty:
            raise ValueError((f'Vegetation type codes for current '
                f'vegetation types not unique:'
                f'{duplicates.sort_values(by=columns)}'))


    def __repr__(self):
        return f'CMSI Vegetationtypes (n={len(self)})'

    def __len__(self):
        return len(self._cmsi_vegtypes)


    def vegetation_types(self, typology='sbb', current_only=True, verbose=False):
        """Return list of vegetation type names and codes for given
        typology.
        
        Parameters
        ----------
        typology : {'sbb','rvvn','vvn'}, default 'sbbcat'
            Name of vegetation typology system.

        current_only : boollean, default True
            Return only vegetation types not deprecated.

        verbose : bool, default False
            Show minimal number of columns (False) or all columns (True).

        Returns
        -------
        DataFrame
            
        """
        typology_name = self.typology_name(typology)
        mask_typology = self._cmsi_vegtypes['VegClas']==typology_name
        vegtypes = self._cmsi_vegtypes[mask_typology].copy()

        if current_only:
            vegtypes = vegtypes[vegtypes['IsCurrent']=='Yes'].copy()

        if not verbose:
            vegtypes = vegtypes[self.VEGTYPECOLS_MINIMAL].copy()

        # turn date into year
        for colname in ['Created', 'Modified']:
            if colname in list(vegtypes):
                vegtypes[colname] = vegtypes[colname].dt.year.copy()

        # set vegetation type code as index and sort index
        vegtypes = vegtypes.set_index('Code', drop=True, verify_integrity=True)
        return vegtypes.sort_index(ascending=True)


    def typology_name(self, typology='sbb'):
        """Return name of typology for given tyopology code.
        
        Parameters
        ----------
        typology : {'sbb','rvvn','vvn'}, default 'sbb'
            Code for typology system.

        Returns
        -------
        str
            Full name of typology
            
        """
        try:
            typology_name = list(filter(lambda x: self.TYPOLOGIES[x] == typology, 
                self.TYPOLOGIES))[0]
        except IndexError as e:
            raise ValueError((f"Unknown typology code '{typology}'. "
                f"Value must be in {list(self.TYPOLOGIES.values())}."))

        return typology_name

    def changes_by_year(self, typology='sbb'):
        """Return table of Creations and Modifications by year for all 
        vegetation types in CMSi.
        
        Parameters
        ----------
        typology : {'sbb','rvvn','vvn'}, default 'sbb'
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
        vegtypes = self.vegetation_types(typology=typology, 
            current_only=False, verbose=True)
        actions = vegtypes[['Created','Modified']].stack().reset_index()
        actions = actions.set_axis(['Code','Action','Year'], axis=1)
        pivot = _pd.pivot_table(data=actions, values='Code', index='Year', 
            columns='Action', aggfunc='count')
        return pivot

    """
    def relations(self, to_typology='rvvn'):

        typology_name = self.get_typology_name(to_typology)

        mask1 = self._cmsi_relations['FROM_VegClas']=='TBO Nationale Vegetatie typologie'
        mask2 = self._cmsi_relations['TO_VegClas']==typology_name
        relations = cmsi._cmsi_relations[mask1&mask2]

        for colname in ['Created', 'Modified']:
            if colname in list(relations):
                relations[colname] = relations[colname].dt.year

        colnames = ['FROM_Code','FROM_ShortScientificName',
            'FROM_LongScientificName','TO_Code','TO_ShortScientificName',
            'TO_LongScientificName','Modified'] #'Created',

        return relations[colnames].set_index('FROM_Code').sort_index()
    """