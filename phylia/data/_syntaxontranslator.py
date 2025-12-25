
import numpy as _np
import pandas as _pd
import re as _re
from ._sbb_revision_2019 import SbbRevision2019
from .cmsi import CmsiSyntaxonTable
from ..tools import syntaxontools

def translate_sbb_to_rvvn(lowest_only=False, include_subass=True):
    """Return table of Staatsbosbeheer Catalogus syntaxa with 
    translation to revision and back.

    Parameters
    ----------
    lowest_only : {'Yes','No'}, default False
        Return translations for lowest level of sbbcat only.
    include_subass : bool, default True
        Translations to sbbcat subassociaties are translated to 
        parent sbbcat associatie.

    Return
    ------
    DataFrame
        Translation of Staatsbosbeheer syntaxa to rvvn syntaxa.
            
    """
    synta = SyntaxonTranslator()
    return synta.translate_sbb_to_rvvn(lowest_only=lowest_only, include_subass=include_subass)


def translate_rvvn_to_sbb(lowest_only=False, include_subass=True):
    """Return table of Revision syntaxa with translation to 
    Staatsbosbeheer Catalogus and back.
    
    Parameters
    ----------
    lowest_only : {'Yes','No'}, default False
        Return translations for lowest level of sbbcat only.
    include_subass : bool, default True
        Translations to sbbcat subassociaties are translated to 
        parent sbbcat associatie.

    Return
    ------
    DataFrame
        Translation of rvvn syntaxa to Staatsbosbeheer syntaxa.
            
    """
    synta = SyntaxonTranslator()
    return synta.translate_rvvn_to_sbb(lowest_only=lowest_only, include_subass=include_subass)


def sbbcrossclasscodes():
    """Return table of crossclasscode for alll class crossing syntaxa in Staatsbosbeheer Catalogus."""
    synta = SyntaxonTranslator()
    return synta.crossclasscodes()


class SyntaxonTranslator:

    JOINSTR = CmsiSyntaxonTable.JOINSTR #', '
    JOINCROSSCLASS = CmsiSyntaxonTable.JOINCROSSCLASS #'#'

    def __init__(self):

        self._cst = CmsiSyntaxonTable()

        self._rev = SbbRevision2019()
        self._translation_rules = self._rev.translations(from_sys='sbbcat', to_sys='rvvn')

        self._sbbcat = self.syntaxa_sbb()
        self._rvvn = self.syntaxa_rvvn()


    def __repr__(self):
        return f"{self.__class__.__name__} (n={len(self)})"

    
    def __len__(self):
        return len(self.translation_rules())


    def syntaxa_sbb(self):
        """Return table of syntaxa from the Staatsbosbeheer Catalogus."""

        # get full table of cmsi sbbcat syntaxa
        sbbcat = self._cst.vegetationtypes(typology='sbbcat', 
            current_only=False, include_mapcodes=False,
            verbose=True)
        ##sbbcat = _vegetationtypes(
        ##    typology='sbbcat', current_only=False, include_mapcodes=False,
        ##    verbose=True)

        # drop confusing columns and rows
        sbbcat = sbbcat.drop(columns=['VegClas', 'GUID', 'Parent', 
            'Description', 'ModifiedBy', 'CreatedBy', 'Quality'])

        return sbbcat


    def syntaxa_rvvn(self):
        """Return table of syntaxaq from the rVVN."""

        # get full table of cmsi revision syntaxa
        rvvn = self._cst.vegetationtypes(typology='rvvn', 
            current_only=False, include_mapcodes=False,
            verbose=True)
        ##rvvn = phylia.data.cmsi.vegetationtypes(
        ##    typology='rvvn', current_only=False, include_mapcodes=False,
        ##    verbose=True)

        # drop confusing columns and rows
        rvvn = rvvn.drop(columns=['VegClas', 'GUID', 'Parent', 
            'Description', 'ModifiedBy', 'CreatedBy', 'Quality'])

        return rvvn


    def _subasscode_to_asscode(self, code, typology='sbbcat'):
        """Return code for associatie given subassociatie."""

        if typology=='sbbcat':
            if self._sbbcat.loc[code,'SynLevel']=='subassociatie':
                code = code[:-1]

        if typology=='rvvn':
            if self._rvvn.loc[code,'SynLevel']=='subassociatie':
                code = code[:-1]

        return code


    def _get_crossclasscode(self, code):
        """Return crossclasscode if syntaxon is class crossing, otherwise return syntaxoncode."""
        crossclasscodes = self.crossclasscodes().to_dict()
        try:
            code = crossclasscodes[code]
        except KeyError:
            code=code
        return code


    def translation_rules(self):
        """Return table of rows with one-to-one translations."""

        # get_translation_rules
        translation_rules = self._translation_rules.copy()

        # add columns for syntaxon status 
        sbb_status = self._sbbcat['IsCurrent'].to_dict()
        translation_rules['sbb_iscurrent'] = translation_rules['code_sbb'].replace(sbb_status)

        sbb_islowest = self._sbbcat['IsLowest'].to_dict()
        translation_rules['sbb_islowest'] = translation_rules['code_sbb'].replace(sbb_islowest)

        rvvn_status = self._rvvn['IsCurrent'].to_dict()
        translation_rules['rvvn_iscurrent'] = translation_rules['code_rvvn_2018'].replace(rvvn_status)

        rvvn_islowest = self._rvvn['IsLowest'].to_dict()
        translation_rules['rvvn_islowest'] = translation_rules['code_rvvn_2018' ].replace(rvvn_islowest)

        translation_rules.index.name = 'translation_id'
        return translation_rules


    def _sbb_to_rvvn(self, lowest_only=False, include_subass=True):
        """Return table of translations from sbbcat to rvvn.
        
        Parameters
        ----------
        lowest_only : {'Yes','No'}
            Return translations for lowest level of rvvn only.
        ingnore_subassociaties :
            Translations to rvvn subassociaties are translated to 
            parent rvvn associatie.

        Return
        ------
        Table with translation of Sbb Catalogus syntaxa to rvvn sysntaxa.
            
        """
        if include_subass:
            # associaties must be present in selection to translate
            # subassociaties to associaties
            lowest_only=False

        translation_rules = self.translation_rules()
        translations = []
        for code, data in translation_rules.groupby('code_sbb'):

            mask_iscurrent = data['rvvn_iscurrent']=='Yes'
            mask_lowest = data['rvvn_islowest']=='Yes'

            # get translations to current rvvn types
            if not lowest_only:
                current = data[mask_iscurrent]['code_rvvn_2018'].values
            else:
                current = data[mask_iscurrent & mask_lowest]['code_rvvn_2018'].values

            if not include_subass:
                # translate rvvn subassociaties to their associaties
                current = sorted(set([self._subasscode_to_asscode(code, 
                    typology='rvvn') for code in current]))

            text_current = self.JOINSTR.join(current) if any(current) else _np.nan

            # get translations historic rvvn types
            if not lowest_only:
                notcurrent = data[~mask_iscurrent]['code_rvvn_2018'].values
            else:
                notcurrent = data[~mask_iscurrent & mask_lowest]['code_rvvn_2018'].values

            if not include_subass:
                # translate rvvn subassociaties to associaties
                notcurrent = sorted(set([self._subasscode_to_asscode(code, 
                    typology='rvvn') for code in notcurrent]))

            text_historic = self.JOINSTR.join(notcurrent) if any(notcurrent) else _np.nan

            # create record with translations
            translations.append({
                'code_sbb':code, 
                'revisie_actueel':text_current,
                'revisie_actueel_count':len(current),
                'revisie_historisch' : text_historic,
                'revisie_historisch_count':len(notcurrent),
                })

        return _pd.DataFrame(translations).set_index('code_sbb', verify_integrity=True)


    def _rvvn_to_sbb(self, lowest_only=False, include_subass=True):
        """Return table of translations from rvvn to sbbcat.

        Parameters
        ----------
        lowest_only : {'Yes','No'}
            Return translations for lowest level of sbbcat only.
        ingnore_subassociaties :
            Translations to sbbcat subassociaties are translated to 
            parent sbbcat associatie.

        Return
        ------
        Table with translation of rvvn syntaxa to Sbb Catalogus syntaxa.
            
        """      
        if include_subass:
            # associaties must be present in selection to translate
            # subassociaties to associaties
            lowest_only=False

        ##translation_rules = self.translation_rules()
        translations = []
        for code, data in self.translation_rules().groupby('code_rvvn_2018'):

            mask_iscurrent = data['sbb_iscurrent']=='Yes'
            mask_lowest = data['sbb_islowest']=='Yes'

            # get translations to current sbb syntaxa

            if not lowest_only:
                current = data[mask_iscurrent]['code_sbb'].values
            else:
                current = data[mask_iscurrent & mask_lowest]['code_sbb'].values

            if not include_subass:
                current = sorted(set([self._subasscode_to_asscode(code, 
                    typology='sbbcat') for code in current]))
            ##current = data[mask_iscurrent]['code_sbb'].values

            # translate to crossclasscodes, if present
            current = sorted(set([self._get_crossclasscode(code) for code in current]))

            # create text line of syntaxa
            current_text = self.JOINSTR.join(current) if any(current) else _np.nan

            # get historic syntaxa
            if not lowest_only:
                notcurrent = data[~mask_iscurrent]['code_sbb'].values
            else:
                notcurrent = data[~mask_iscurrent & mask_lowest]['code_sbb'].values
            ##notcurrent = data[~mask_iscurrent]['code_sbb'].values
            historic_text = self.JOINSTR.join(notcurrent) if any(notcurrent) else _np.nan

            translations.append({
                'code_rvvn' : code, 
                'sbbcat_vertaling' : current_text,
                'sbbcat_vertaling_historisch' : historic_text,
                'sbbcat_vertaling_count' : len(current),
                'sbbcat_vertaling_historisch_count' : len(notcurrent),
                })

        return _pd.DataFrame(translations).set_index('code_rvvn', verify_integrity=True)


    def _sbb_back_to_sbb(self, lowest_only=False, include_subass=True):
        """Return table of translationa from sbbcat to rvvn and back again."""

        sbb_naar_revisie = self._sbb_to_rvvn(lowest_only=lowest_only, 
            include_subass=include_subass)
        revisie_naar_sbb = self._rvvn_to_sbb(lowest_only=lowest_only, 
            include_subass=include_subass)

        # translation back to sbbcat
        sbb_naar_revisie['sbb_terugvertaling'] = _pd.Series(dtype='object')
        sbb_naar_revisie['sbb_terugvertaling_count'] = _pd.Series(dtype='int')
        for idx in sbb_naar_revisie.index:
            revisie_codes = sbb_naar_revisie.loc[idx,'revisie_actueel']
            
            if isinstance(revisie_codes, float):
                sbb_naar_revisie.loc[idx,'sbb_terugvertaling'] = _np.nan
                sbb_naar_revisie.loc[idx,'sbb_terugvertaling_count'] = 0
                continue

            sbb_list = []
            for rvvncode in revisie_codes.split(self.JOINSTR):
                sbb_vertaling = revisie_naar_sbb.loc[rvvncode.strip(),'sbbcat_vertaling']
                if _pd.isnull(sbb_vertaling):
                    continue

                #sbb_vertaling_codes = [x.strip() for x in sbb_vertaling.split(self.JOINSTR)]
                sbb_vertaling_codes = _re.split(f'{self.JOINSTR}|{self.JOINCROSSCLASS}', sbb_vertaling)

                if not lowest_only:
                    sbb_list.extend(sbb_vertaling_codes)
                else:
                    for code in sbb_vertaling_codes:
                        if sbb_islowest[code]=='Yes':
                            sbb_list.extend([code])
                sbb_vertaling_codes = sbb_list.copy()


            if not include_subass:
                sbb_vertaling_codes = sorted(set([self._subasscode_to_asscode(code, 
                    typology='sbbcat') for code in sbb_vertaling_codes]))

            # translate to crossclasscodes, if present
            sbb_vertaling_codes = sorted(set([self._get_crossclasscode(code) 
                for code in sbb_vertaling_codes]))


            sbb_naar_revisie.loc[idx,'sbb_terugvertaling'] = self.JOINSTR.join(sorted(set(sbb_vertaling_codes)))
            sbb_naar_revisie.loc[idx,'sbb_terugvertaling_count'] = len(set(sbb_vertaling_codes))
        sbb_naar_revisie['sbb_terugvertaling_count'] = sbb_naar_revisie['sbb_terugvertaling_count'].astype(int)
        return sbb_naar_revisie


    def _rvvn_back_to_rvvn(self, lowest_only=False, include_subass=True):
        """Return table of translations from rvvn to sbbcat and back again."""

        if include_subass:
            lowest_only=False

        revisie_naar_sbb = self._rvvn_to_sbb(lowest_only=lowest_only, include_subass=include_subass)
        sbb_naar_revisie = self._sbb_to_rvvn(lowest_only=lowest_only, include_subass=include_subass)

        # translation back to revisie
        revisie_naar_sbb['revisie_terugvertaling'] = _pd.Series(dtype='object')
        revisie_naar_sbb['revisie_terugvertaling_count'] = _pd.Series(dtype='object')
        for idx in revisie_naar_sbb.index:
            sbb_codes = revisie_naar_sbb.loc[idx,'sbbcat_vertaling']
            if isinstance(sbb_codes, float):
                revisie_naar_sbb.loc[idx,'revisie_terugvertaling'] = _np.nan
                revisie_naar_sbb.loc[idx,'revisie_terugvertaling_count'] = 0
                continue

            revisie_list = []
            sbb_codes = _re.split(f'{self.JOINSTR}|{self.JOINCROSSCLASS}', sbb_codes)
            for code in sbb_codes:
                revisie_vertaling = sbb_naar_revisie.loc[code.strip(),'revisie_actueel']
                if _pd.isnull(revisie_vertaling):
                    continue
                revisie_vertaling_codes = [x.strip() for x in revisie_vertaling.split(self.JOINSTR)]

                if not lowest_only:
                    revisie_list.extend(revisie_vertaling_codes)
                else:
                    for code in revisie_vertaling_codes:
                        if rvvn_islowest[code]=='Yes':
                            revisie_list.extend([code])
                revisie_vertaling_codes = revisie_list.copy()

            if not include_subass:
                revisie_vertaling_codes = sorted(set([self._subasscode_to_asscode(code, 
                    typology='rvvn') for code in revisie_vertaling_codes]))

            revisie_naar_sbb.loc[idx,'revisie_terugvertaling'] = self.JOINSTR.join(sorted(set(revisie_vertaling_codes)))
            revisie_naar_sbb.loc[idx,'revisie_terugvertaling_count'] = len(set(revisie_vertaling_codes))

        return revisie_naar_sbb


    def crossclasscodes(self):
        """Return table of crossclasscode for alll class crossing syntaxa in Staatsbosbeheer Catalogus."""
        return self._sbbcat[self._sbbcat['CrossClassCodes'].notnull()]['CrossClassCodes']


    def translate_sbb_to_rvvn(self, lowest_only=False, include_subass=True):
        """Return table of Staatsbosbeheer Catalogus syntaxa with 
        translation to revision and back.

        Parameters
        ----------
        lowest_only : {'Yes','No'}, default False
            Return translations for lowest level of sbbcat only.
        include_subass : bool, default True
            Translations to sbbcat subassociaties are translated to 
            parent sbbcat associatie.

        Return
        ------
        DataFrame
            Translation of Staatsbosbeheer syntaxa to rvvn syntaxa.
                
        """
        translations = self._sbb_back_to_sbb(
            lowest_only=lowest_only, include_subass=include_subass)
           
        translations = translations.rename(columns={
            'revisie_actueel':'RevisieVertaling',
            'sbb_terugvertaling':'SbbTerugvertaling',
            'revisie_historisch':'RevisieVertalingHistorisch',
            'revisie_actueel_count':'RevisieVertalingCount',
            'revisie_historisch_count':'RevisieVertalingHistorischCount',
            'sbb_terugvertaling_count':'SbbTerugvertalingCount',
            })

        cmsi_sbb = self.syntaxa_sbb()
        cmsi_rev = self.syntaxa_rvvn()

        # merge translations to cmsi_sbb
        cmsi_sbb = _pd.merge(cmsi_sbb, translations, left_index=True, right_index=True, how='left')
        for column in ['RevisieVertalingCount', 'RevisieVertalingHistorischCount', 
            'SbbTerugvertalingCount', 'RevisieVertalingHistorischCount']:
            cmsi_sbb[column] = cmsi_sbb[column].fillna(0).astype(int)

        # add column with RevisieVertalingLevel
        mask = cmsi_sbb['RevisieVertalingCount']==1
        cmsi_sbb.loc[mask,'RevisieVertalingLevel'] = cmsi_sbb.loc[mask,'RevisieVertaling'].apply(
            phylia.tools.syntaxontools.syntaxonlevel, reference='rvvn')

        # add column RevisieVertalingIsLowest
        rvvn_codes = cmsi_rev[cmsi_rev['IsLowest']=='Yes'].index.values
        cmsi_sbb['RevisieVertalingIsLowest'] = cmsi_sbb['RevisieVertaling'].apply(
            lambda x: 'Yes' if x in rvvn_codes else 'No')
       
        # identical syntaxa
        mask1 = cmsi_sbb['RevisieVertalingCount']==1
        mask2 = cmsi_sbb['SbbTerugvertalingCount']==1
        cmsi_sbb.loc[(mask1&mask2),'RevisieIdentiek'] = 'Yes'
        cmsi_sbb.loc[(~mask1|~mask2),'RevisieIdentiek'] = 'No'
        assert cmsi_sbb[cmsi_sbb['RevisieIdentiek'].isna()].empty

        columns = ['RevisieVertaling', 'RevisieVertalingHistorisch',
            'SbbTerugvertaling', 'IsCurrent', 'IsLowest', 'IsCrossClass',
            'CrossClassCodes', 'SynLevel', 'SynClass', 
            'RevisieVertalingLevel', 'RevisieVertalingIsLowest', 
            'RevisieIdentiek', 'RevisieVertalingCount',
            'RevisieVertalingHistorischCount', 'SbbTerugvertalingCount',
            'ShortScientificName', 'LongScientificName', 
            'ShortCommonName', 'LongCommonName', 'Created', 'Modified',
            ]
        missing = [x for x in cmsi_sbb.columns if x not in columns]
        if missing:
            raise ValueError((f"Missing column {missing}"))
        return cmsi_sbb[columns]


    def translate_rvvn_to_sbb(self, lowest_only=False, include_subass=True):
        """Return table of Revision syntaxa with translation to 
        Staatsbosbeheer Catalogus and back.
        
        Parameters
        ----------
        lowest_only : {'Yes','No'}, default False
            Return translations for lowest level of sbbcat only.
        include_subass : bool, default True
            Translations to sbbcat subassociaties are translated to 
            parent sbbcat associatie.

        Return
        ------
        DataFrame
            Translation of rvvn syntaxa to Staatsbosbeheer syntaxa.
                
        """

        translations = self._rvvn_back_to_rvvn(
            lowest_only=lowest_only, include_subass=include_subass).rename(
            columns={
            'sbbcat_vertaling':'SbbVertaling',
            'revisie_terugvertaling' : 'RevisieTerugvertaling',
            'sbbcat_vertaling_count' : 'SbbVertalingCount',
            'sbbcat_vertaling_historisch_count' : 'SbbVertalingHistorischCount',
            'revisie_terugvertaling_count' : 'RevisieTerugvertalingCount',
            'sbbcat_vertaling_historisch':'SbbVertalingHistorisch',
            })

        cmsi_rev = self._rvvn.copy()
        cmsi_sbb = self._sbbcat.copy()

        # merge translations to cmsi_rev
        cmsi_rev = _pd.merge(cmsi_rev, translations, left_index=True, right_index=True, how='left')
        cmsi_rev['SbbVertalingCount'] = cmsi_rev['SbbVertalingCount'].fillna(0).astype(int)
        cmsi_rev['RevisieTerugvertalingCount'] = cmsi_rev['RevisieTerugvertalingCount'].astype(float).fillna(0).astype(int)

        # add column with SbbVertalingLevel
        mask = cmsi_rev['SbbVertalingCount']==1
        cmsi_rev['SbbVertalingLevel'] = cmsi_rev['SbbVertaling']
        cmsi_rev.loc[~mask, 'SbbVertalingLevel'] = _np.nan
        cmsi_rev['SbbVertalingLevel'] = cmsi_rev['SbbVertalingLevel'].str.split(
            self.JOINCROSSCLASS, n=1, expand=True)[0]
        cmsi_rev['SbbVertalingLevel'] = cmsi_rev['SbbVertalingLevel'].apply(
            syntaxontools.syntaxonlevel, reference='sbbcat').fillna(_np.nan)

        # add column SbbVertalingIsLowest
        sbb_codes = cmsi_sbb[cmsi_sbb['IsLowest']=='Yes'].index.values
        sr = cmsi_rev['SbbVertaling'].str.split(self.JOINCROSSCLASS, n=1, expand=True)[0].squeeze()
        cmsi_rev['SbbVertalingIsLowest'] = sr.apply(
            lambda x: 'Yes' if x in sbb_codes else 'No')

        # identical syntaxa
        mask1 = cmsi_rev['SbbVertalingCount']==1
        mask2 = cmsi_rev['RevisieTerugvertalingCount']==1
        cmsi_rev.loc[mask1&mask2,'SbbIdentiek'] = 'Yes'
        cmsi_rev.loc[(~mask1|~mask2),'SbbIdentiek'] = 'No'
        assert cmsi_rev[cmsi_rev['SbbIdentiek'].isna()].empty

        columns = [
            'SbbVertaling',
            'SbbVertalingHistorisch',
            'RevisieTerugvertaling',
            'SbbVertalingLevel',
            'SbbVertalingIsLowest',
            'SbbIdentiek',
            'IsCurrent',
            'SynLevel',
            'SynClass',
            'IsLowest',
            'SbbVertalingCount',
            'SbbVertalingHistorischCount',
            'RevisieTerugvertalingCount',
            'ShortScientificName',
            'LongScientificName',
            'ShortCommonName',
            'LongCommonName',
            'Created',
            'Modified',
            ]
        missing = [x for x in cmsi_rev.columns if x not in columns]
        if missing:
            raise ValueError((f"Missing column {missing}"))
        return cmsi_rev[columns]
