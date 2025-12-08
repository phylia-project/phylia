"""Class CmsiVegtypes holds lists of vegetation types used in CMSi."""

import numpy as _np
from pandas import Series, DataFrame
import pandas as _pd
from importlib import resources as _resources

import logging as _logging
_logger = _logging.getLogger(__name__)

from . import _data_cmsi
from ..tools import syntaxontools as _syntaxontools

def vegetationtypes(typology='sbbcat', current_only=True, 
    include_mapcodes=True, include_crossclass=True, verbose=False):
    """Return list of vegetation type names and codes for given
    typology.
    
    Parameters
    ----------
    typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
        Name of vegetation typology system.

    current_only : boollean, default True
        Return only vegetation types not deprecated.

    include_mapcodes : bool, default True
        If True, include mapping codes that do not represent a real syntaxon 
        (like pavements and non-mapped areas).

    include_crossclass : bool, default True
        Include all occurences of class crossing syntaxa (True) or 
        only the first occurrence (False). This only applies to the 
        Staatsbosbeheer Catalogus reference system.

    verbose : bool, default False
        Show minimal number of columns (False) or all columns (True).

    Returns
    -------
    DataFrame
        
    """
    cst = CmsiSyntaxonTable()
    syntaxa = cst.vegetationtypes(typology=typology, 
        current_only=current_only, include_mapcodes=include_mapcodes,
        verbose=verbose)
    return syntaxa


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

    JOINSTR = ', '
    JOINCROSSCLASS = '#'

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

    VEGTYPECOLS_MINIMAL = ['Code', 'LongScientificName', 'LongCommonName',
        'Created', 'IsCurrent', 'SynLevel', 'SynClass', 'IsLowest',]

    SBBCAT_MAPPINGCODES = ['50A', '50B', '50C', '100', '200', '300', '400',]

    RVVN_MAPPINGCODES = ['r50A', 'r50B', 'r50C', 'r100', 'r200', 'r300', 'r400',]


    def __init__(self):

        # get table of cmsi vegetation types from package data
        srcfile = (_resources.files(_data_cmsi) / 'CMSiVegetationTypes.csv')
        self._syntaxa_src = _pd.read_csv(srcfile, sep=';', encoding='utf-8', dtype='object')

        self._syntaxa = self._syntaxa_src.copy()
        self._syntaxa['IsCurrent'] = self._syntaxa['IsCurrent'].replace({'1':'Yes', '0':'No'})


        # BUGFIXES: correct typos in CmsiTable syntaxa
        # ------------------------------------------

        # 43C1g NotCurrent
        idx = self._syntaxa[self._syntaxa['Code']=='43C1g'].index.values[0]
        if self._syntaxa.at[idx,'IsCurrent']=='Yes':
            self._syntaxa.at[idx,'IsCurrent']='No'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for 43C1g can be removed.')            

        # set three KOV syntaxa from vervallen to IsCurrent
        for sbbcode in ['43B-b', '43-j', '22B-a']:
            idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
            if self._syntaxa.at[idx,'IsCurrent']=='No':
                self._syntaxa.at[idx,'IsCurrent'] = 'Yes'
            else:
                _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        # Drop non-existent Revisie syntaxon
        code = 'r40RG01'
        if not self._syntaxa[self._syntaxa['Code']==code].empty:
            idx = self._syntaxa[self._syntaxa['Code']==code].index.values[0]
            self._syntaxa = self._syntaxa.drop(idx)
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for Revisie syntaxon {code} can be removed.')

        # BUFIX: Correct names for klasseoverschrijdende syntaxa
        # ------------------------------------------------------

        sbbcode = '05-a'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongScientificName']=='RG Potamogeton natans-[Potametea]':
            self._syntaxa.loc[idx,'LongScientificName']='RG Potamogeton natans-[Potametea/Lemnetea minoris]'
            self._syntaxa.loc[idx,'ShortScientificName']='RG Potamogeton natans-[Potametea/Lemnetea minoris]'
            self._syntaxa.loc[idx,'LongCommonName']='RG Drijvend fonteinkruid [Fonteinkruiden-klasse/Eendenkroos-klasse]'
            self._syntaxa.loc[idx,'ShortCommonName']='RG Drijvend fonteinkruid [Fonteinkruiden-klasse/Eendenkroos-klasse]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        sbbcode = '04A-a'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongScientificName']=='RG Nitella flexilis-[Nitellion flexilis]':
            self._syntaxa.loc[idx,'LongScientificName']='RG Nitella flexilis-[Nitellion flexilis/Potametea]'
            self._syntaxa.loc[idx,'ShortScientificName']='RG Nitella flexilis-[Nitellion flexilis/Potametea]'
            self._syntaxa.loc[idx,'LongCommonName']='RG Buigzaam glanswier [Kranswieren-klasse/Fonteinkruiden-klasse]'
            self._syntaxa.loc[idx,'ShortCommonName']='RG Buigzaam glanswier [Kranswieren-klasse/Fonteinkruiden-klasse]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        sbbcode = '05/a'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongScientificName']=='DG Myriophyllum aquaticum-[Potametea]':
            self._syntaxa.loc[idx,'LongScientificName']='DG Myriophyllum aquaticum-[Potametea/Phragmitetea]'
            self._syntaxa.loc[idx,'ShortScientificName']='DG Myriophyllum aquaticum-[Potametea/Phragmitetea]'
            self._syntaxa.loc[idx,'LongCommonName']='DG Parelvederkruid [Riet-klasse/Fonteinkruiden-klasse]'
            self._syntaxa.loc[idx,'ShortCommonName']='DG Parelvederkruid [Riet-klasse/Fonteinkruiden-klasse]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        sbbcode = '08/b'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongScientificName']=='DG Myriophyllum aquaticum-[Phragmitetea]':
            self._syntaxa.loc[idx,'LongScientificName']='DG Myriophyllum aquaticum-[Potametea/Phragmitetea]'
            self._syntaxa.loc[idx,'ShortScientificName']='DG Myriophyllum aquaticum-[Potametea/Phragmitetea]'
            self._syntaxa.loc[idx,'LongCommonName']='DG Parelvederkruid [Riet-klasse/Fonteinkruiden-klasse]'
            self._syntaxa.loc[idx,'ShortCommonName']='DG Parelvederkruid [Riet-klasse/Fonteinkruiden-klasse]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        sbbcode = '32/b'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongScientificName']=='DG Impatiens glandulifera-[Convolvulo-Filipenduletea]':
            self._syntaxa.loc[idx,'LongScientificName']='DG Impatiens glandulifera-[Conv-Filipen/Galio-Urticetea]'
            self._syntaxa.loc[idx,'ShortScientificName']='DG Impatiens glandulifera-[Convolvulo-Filipenduletea/Galio-Urticetea]'
            self._syntaxa.loc[idx,'LongCommonName']='DG Reuzenbalsemien-[Klasse der natte strooiselruigten/Klasse van de nitrofiele zomen]'
            self._syntaxa.loc[idx,'ShortCommonName']='DG Reuzenbalsemien-[Klasse der natte strooiselruigten/Klasse van de nitrofiele zomen]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        sbbcode = '33/e'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongScientificName']=='DG Impatiens glandulifera-[Galio-Urticetea]':
            self._syntaxa.loc[idx,'LongScientificName']='DG Impatiens glandulifera-[Conv-Filipen/Galio-Urticetea]'
            self._syntaxa.loc[idx,'ShortScientificName']='DG Impatiens glandulifera-[Convolvulo-Filipenduletea/Galio-Urticetea]'
            self._syntaxa.loc[idx,'LongCommonName']='DG Reuzenbalsemien-[Klasse der natte strooiselruigten/Klasse van de nitrofiele zomen]'
            self._syntaxa.loc[idx,'ShortCommonName']='DG Reuzenbalsemien-[Klasse der natte strooiselruigten/Klasse van de nitrofiele zomen]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        # BUFIX: Derivaat not changed to Romp
        sbbcode = '06/b'
        idx = self._syntaxa[self._syntaxa['Code']==sbbcode].index.values[0]
        if self._syntaxa.loc[idx,'LongCommonName']=='RG Watercrassula [Oeverkruid-klasse]':
            self._syntaxa.loc[idx,'LongCommonName']='DG Watercrassula [Oeverkruid-klasse]'
            self._syntaxa.loc[idx,'ShortCommonName']='DG Watercrassula [Oeverkruid-klasse]'
        else:
            _logger.warning(f'Bugfix in CmsiSyntaxonTable.init for {sbbcode} can be removed.')

        # BUGFIX: LongScientificNames with -etalia
        veg = self._syntaxa.copy()
        mask=veg['VegClas']=='TBO Nationale Vegetatie typologie'
        veg = veg[mask].copy()
        # add column with syntaxlevel
        veg['SynLevel'] = _pd.Categorical(
            values = veg['Code'].apply(
            _syntaxontools.syntaxonlevel, reference='sbbcat'),
            categories = self.SYNTAXON_ORDER,
            ordered=True,
            )
        mask = veg['LongScientificName'].str.endswith('alia')
        mask2 = veg['SynLevel']=='verbond'
        if veg[mask&mask2].empty:
            print(f"Bugfix for LongScientificnames with -etalia can be removed.")
        if not veg[mask&mask2].empty:
            for idx, row in veg[mask&mask2].iterrows():
                mask = self._syntaxa['GUID']==row['GUID']
                idx = self._syntaxa[mask].index[0]
                self._syntaxa.loc[idx,'LongScientificName']=self._syntaxa.loc[idx,'ShortScientificName']


        # validate spelling of syntaxon codes
        # (in CMSi the codes of the VVN sytem are spelled with capitals)
        self._syntaxa['Code'] = _syntaxontools.syntaxon_validate(
            self._syntaxa['Code'])

        # convert datetime columns
        for colname in ['Created','Modified']:
            self._syntaxa[colname] = _pd.to_datetime(
                self._syntaxa[colname], format='ISO8601')

        # make field IsCurrent Categorical
        self._syntaxa['IsCurrent'] = _pd.Categorical(
            values = self._syntaxa['IsCurrent'], 
            categories=['Yes','No'], 
            ordered=True,
            )

        # convert field Quality from float to str
        self._syntaxa['Quality'] = self._syntaxa['Quality'].astype(str).str.split('.').str[0]
        self._syntaxa['Quality'] = self._syntaxa['Quality'].replace('nan', _np.nan)

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


    def __repr__(self):
        return f'CMSI Vegetationtypes (n={len(self)})'


    def __len__(self):
        return len(self._syntaxa)


    def vegetationtypes(self, typology='sbbcat', current_only=True, include_mapcodes=True,
        include_crossclass=True, verbose=False):
        """Return list of vegetation type names and codes for given
        typology.
        
        Parameters
        ----------
        typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
            Name of vegetation typology system.

        current_only : bool, default True
            Return only vegetation types not deprecated.

        include_mapcodes : bool, default True
            Drop codes that are used for mapping polygons that do not 
            represent a real syntaxon (like pavements and non-mapped areas).

        include_crossclass : bool, default True
            Include all occurences of class crossing syntaxa (True) or 
            only the first occurrence (False). This only applies to the 
            Staatsbosbeheer Catalogus reference system.

        verbose : bool, default False
            Show minimal number of columns (False) or all columns (True).

        Returns
        -------
        DataFrame
            
        """

        # get syntaxa for chosen typology
        mask = self._syntaxa['VegClas']==self.typology_longname(typology)
        vegtypes = self._syntaxa[mask].copy()

        # set syntaxcode as index
        vegtypes = vegtypes.set_index('Code', drop=True, 
            verify_integrity=True).sort_index(ascending=True)

        # turn date into year
        for colname in ['Created', 'Modified']:
            if colname in list(vegtypes):
                vegtypes[colname] = vegtypes[colname].dt.year.astype('str')

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

        if not verbose:
            colnames = [x for x in self.VEGTYPECOLS_MINIMAL if x!='Code']
            vegtypes = vegtypes[colnames].copy()

        if typology=='sbbcat':

            # add empty columns with codes for class crossing syntaxa
            vegtypes['IsCrossClass'] = 'No'
            vegtypes['CrossClassCodes'] = _np.nan
            vegtypes['CrossClassCodes'] = vegtypes['CrossClassCodes'].astype('object')

            # fill in crossclasscodes
            iscurrent = vegtypes['IsCurrent']=='Yes' # 43C1 is called Stellario-Carpinetum
            for name, df in vegtypes[iscurrent].groupby('LongScientificName'):
                if len(df)>1:
                    codestring = self.JOINCROSSCLASS.join((df.index.values))
                    vegtypes.loc[df.index, 'IsCrossClass'] = 'Yes'
                    vegtypes.loc[df.index, 'CrossClassCodes'] = codestring

            vegtypes['IsCrossClass'] = _pd.Categorical(
                values = vegtypes['IsCrossClass'], 
                categories=['Yes','No'], 
                ordered=True,
                )

            if not include_mapcodes:
                # drop maping codes that do not represent a syntaxon
                vegtypes = vegtypes.drop(labels=self.SBBCAT_MAPPINGCODES)

            if not include_crossclass:
                # select only first occurrence of a syntaxon
                selection = vegtypes.reset_index(drop=False).groupby('LongScientificName').first()
                vegtypes = vegtypes.loc[selection['Code'].values, :].sort_index()

        if typology=='rvvn':

            if not include_mapcodes:
                # drop maping codes that do not represent a syntaxon
                vegtypes = vegtypes.drop(labels=self.RVVN_MAPPINGCODES)

        if current_only:
            vegtypes = vegtypes[vegtypes['IsCurrent']=='Yes'].copy()

        return vegtypes.sort_index()


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
        The result shows changes in de list of vegetation types in CMSi. 
        It is not a table of changes in de typology system itself.
            
        """
        vegtypes = self.vegetationtypes(typology=typology, 
            current_only=False, include_mapcodes=False, 
            include_crossclass=True, verbose=True)
        actions = vegtypes[['Created','Modified']].stack().reset_index()
        actions = actions.set_axis(['Code','Action','Year'], axis=1)
        pivot = _pd.pivot_table(data=actions, values='Code', index='Year', 
            columns='Action', aggfunc='count')
        return pivot

    def mapcodes(self, typology='sbbcat'):
        """Return table of codes used for mapping non-syntaxon polygons,
        like water, pavements and unknown vegetation types.

        Parameters
        ----------
        typology : {'sbbcat','rvvn','vvn'}, default 'sbbcat'
            Code for typology system.

        Returns
        -------
        DataFrame
            Table of changes by year.
             
        """
        syntaxa = self.vegetationtypes(typology=typology, current_only=False, 
            include_mapcodes=True, verbose=False)

        # get list of mapping codes
        if typology=='sbbcat':
            codes = self.SBBCAT_MAPPINGCODES
        elif typology=='rvvn':
            codes = self.RVVN_MAPPINGCODES
        elif typology=='vvn':
            codes = []
        else:
            raise ValueError(f'Invalid classification system code {typology}')

        # select from syntaxa tables
        mapcodes = syntaxa.loc[codes,'LongScientificName'].squeeze()
        mapcodes.name = 'mapcodes'
        return mapcodes


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


    def get_planten(self):
        """Return table of plant names."""
        mask = self._taxon_preferred['TaxonGroupName'].isin(['Vaatplanten','Korstmossen','Mossen','Kranswieren',])
        return self._taxon_preferred[mask]



