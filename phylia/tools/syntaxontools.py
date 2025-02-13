"""Module with functions for validating and inspecting syntaxon codes."""

import re as _re
import numpy as _np
import pandas as _pd
import logging as _logging
_logger = _logging.getLogger(__name__)


SUPPORTED_REFERENCE_SYSTEMS = ['sbbcat', 'vvn', 'rvvn']

SBB_PATTERNS = {
    'klasse': r'(^[0-4]?[0-9]$)', # '(05)'
    'klasseromp' : r'(^[0-4]?[0-9])(-)([A-Za-z]{1}$)', # '(05)(-)(a)'
    'klassederivaat' : r'(^[0-4]?[0-9])(/|%)([A-Za-z]{1}$)', # '(05)(%)(a)'
    'verbond' : r'(^[0-4]?[0-9])([A-Za-z]{1}$)', # '(05)(A)'
    'verbondsromp' : r'(^[0-4]?[0-9])([A-Za-z]{1})(-)([A-Za-z]$)', # '(05)(A)(-)(a)'
    'verbondsderivaat' : r'(^[0-4]?[0-9])([A-Za-z]{1})(/|%)([A-Za-z]$)', # '(05)(A)(%)(a)'
    'associatie' : r'(^[0-4]?[0-9])([A-Za-z]{1})([0-9]{1,2}$)', # '(05)(A)(10)'
    'subassociatie' :  r'(^[0-4]?[0-9])([A-Za-z]{1})([0-9]{1,2})([A-Za-z]$)', # '(05)(A)(10)(a)
    'nvt' : r'^(50[A-Z]|400|300|200|100)$', # '(50A)'
    }

VVN_PATTERNS = {
    'klasse' : r'(^r?)([0-4]?[0-9]$)', # '(r)(05)'
    'orde' : r'(^r?)([0-4]?[0-9])([A-Za-z]$)', # '(r)(05)(A)'
    'verbond' : r'(^r?)([0-4]?[0-9])([A-Za-z])([A-Za-z]$)', # '(r)(05)(A)(a)'
    'associatie': r'(^r?)([0-4]?[0-9])([A-Za-z])([A-Fa-f])([0-9]?[0-9]$)', # '(r)(05)(A)(a)(1)'
    'subassociatie': r'(^r?)([0-4]?[0-9])([A-Za-z])([A-Fa-f])([0-9]?[0-9])([A-Za-z]$)', # '(r)(05)(A)(a)(1)(a)'
    'romp': r'(^r?)([0-4]?[0-9])([Rr][Gg])([0-9]?[0-9]$)', # '(r)(05)(RG)(01)'
    'derivaat': r'(^r?)([0-4]?[0-9])([Dd][Gg])([0-9]?[0-9]$)', # '(r)(05)(DG)(01)'
    'nvt' : r'(^r?)(50[A-Z]|400|300|200|100)$', #'(r)(50A)' | '(r)(100)'
    }


SYNTAXON_ORDER = ['klasse', 'orde', 'verbond', 'associatie', 
    'subassociatie', 'klasseromp', 'verbondsromp', 'romp',
    'klassederivaat', 'verbondsderivaat', 'derivaat',
     ]

SBB_TESTCODES = ['05', '05-a', '05/a', '05%a', '05A', '05A-a', 
    '05A/a', '05A%a', '05A1', '05A1a','5','5-A','5/A','5%A',
    '5a', '5a-A', '5a/A', '5a%A', '5a1', '5a1A', '50A', '200',]

VVN_TESTCODES = ['r05', 'r05A', 'r05Aa', 'r05Aa1', 'r05Aa1a',
    'r50A', 'r200',
    '05', '05A', '05Aa', '05Aa1', '05Aa1a', 'r5', 'r5a', 
    '50A', '200',
    'r5aA1', 'r5aA1A', 'rubbish',]



def reference_patterns(reference='sbbcat'):
    """Return dictionary of regular expression patterns for all 
    possible syntaxonomic levels.
    
    Parameters
    ----------
    reference : {'sbbcat', 'rvvn', 'vvn'}, default 'sbbcat'
        Reference system for syntaxonomical units.

    Returns
    -------
    dictionary | None
        (syntaxonomical level, pattern)
            
    """
    if reference=='sbbcat':
        return SBB_PATTERNS
    elif reference in ['vvn', 'rvvn']:
        return VVN_PATTERNS
    else:
        _logger.error(f'Reference system "{reference}" is not supported.')
    return None


def reference_levels(reference='sbbcat'):
    """Return list of all valid syntaxon levels.

    Parameters
    ----------    
    reference : {'sbbcat', 'rvvn', 'vvn'}, default 'sbbcat'
        Syntaxonomic reference system.

    Returns
    -------
    list
        [syntaxonomical levels]
            
    """
    if reference=='sbbcat':
        return list(SBB_PATTERNS.keys())
    elif reference in ['vvn','rvvn']:
        return list(VVN_PATTERNS.keys())
    else:
        _logger.error(f'Reference system "{reference}" is not supported.')
    return None


def _syntaxon_validate_string(code):
    """Validate string as syntaxoncode and return valid syntaxon 
    code. This is a helper function for syntaxon_validate() method."""

    if _pd.isnull(code):
        return np.nan

    newtext = None # if no match is found, None will be the returned result

    # First, test for sbbcat patterns
    for syntaxlevel, pattern in SBB_PATTERNS.items():

        if _re.search(pattern, code, flags=_re.IGNORECASE):

            if syntaxlevel=='klasse':
                callback = lambda pat: pat.group(1).zfill(2)
            if syntaxlevel=='klasseromp':
                callback = lambda pat: pat.group(1).zfill(2)+pat.group(2)+pat.group(3).lower()
            if syntaxlevel=='klassederivaat':
                callback = lambda pat: pat.group(1).zfill(2)+pat.group(2)+pat.group(3).lower()
            if syntaxlevel=='verbond':
                callback = lambda pat: pat.group(1).zfill(2)+pat.group(2).upper()
            if syntaxlevel=='verbondsromp':
                callback = lambda pat: pat.group(1).zfill(2)+pat.group(2).upper()+pat.group(3)+pat.group(4).lower()
            if syntaxlevel=='verbondsderivaat':
                callback = lambda pat: pat.group(1).zfill(2)+pat.group(2).upper()+pat.group(3)+pat.group(4).lower()
            if syntaxlevel=='associatie':
                callback = lambda pat: pat.group(1).zfill(2)+pat.group(2).upper()+pat.group(3)
            if syntaxlevel=='subassociatie':
                callback = (lambda pat: pat.group(1).zfill(2)+pat.group(2).upper()+pat.group(3)+pat.group(4).lower())
            if syntaxlevel=='nvt':
                callback = (lambda pat: pat.group(1))

            newtext = _re.sub(pattern, callback, code)
            return newtext # pattern from SbbCat recognised, return result

    # Second, no match was found to sbbcat, test for rvvn patterns
    for syntaxlevel, pattern in VVN_PATTERNS.items():

        if _re.search(pattern, code):

            if syntaxlevel=='klasse':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    )
            if syntaxlevel=='orde':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    +pat.group(3).upper()
                    )
            if syntaxlevel=='verbond':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    +pat.group(3).upper()
                    +pat.group(4).lower()
                    )
            if syntaxlevel=='associatie':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    +pat.group(3).upper()
                    +pat.group(4).lower()
                    +pat.group(5)
                    )
            if syntaxlevel=='subassociatie':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    +pat.group(3).upper()
                    +pat.group(4).lower()
                    +pat.group(5)
                    +pat.group(6).lower()
                    )
            if syntaxlevel=='romp':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    +pat.group(3).upper()
                    +pat.group(4).zfill(2)
                    )
            if syntaxlevel=='derivaat':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2).zfill(2)
                    +pat.group(3).upper()
                    +pat.group(4).zfill(2)
                    )
            if syntaxlevel=='nvt':
                callback = (lambda pat: pat.group(1).lower()
                    +pat.group(2)
                    )

            newtext = _re.sub(pattern, callback, code)
            return newtext # pattern from VVN recognised, return result

    # Third, no match was found at all, return None
    return newtext


def syntaxon_validate(code):
    """Return validated syntaxoncode.
    
    Parameters
    ----------
    code : pandas.Series | list | str
        Syntaxoncode text.

    Returns
    -------
    pd.Series | str | np.nan
        Valid syntaxon code.

    Notes
    -----
    Any text that resembles a valid syntaxon code in either the 
    Staatsbosbeheer Catalogus reference system of the Vegetatie 
    van Nederland reference system will be returned as a valid 
    syntaxon code. When no match is found, the result will be None.
        
    """

    if isinstance(code, _pd.Series):
        validated = code.apply(_syntaxon_validate_string)
        return validated

    if isinstance(code, list):
        if all(isinstance(item, str) for item in code):
            validated = [_syntaxon_validate_string(x) for x in code]
            return validated
        else:
            raise ValueError((f'Not all syntaxoncodes are of type '
                f'string: "{code}".'))

    if _pd.isnull(code):
        _logger.error((f'Input "{code}" of type {type(code)} is no valid '
            f'syntaxon input'))
        return None

    if isinstance(code, int):
        code = str(code)

    if isinstance(code, float):
        code = str(code)

    if isinstance(code, str):
        validated = _syntaxon_validate_string(code)
        if not validated:
            _logger.error(f'No matching pattern found for "{code}"')      
        return validated

    raise ValueError((f'Unknown type for syntaxon code: {type(code)}'))


def _syntaxonclass_string(code):
    """Return number of syntaxonomical class given a valid syntaxon code.
    This is a helper function for syntaxonclass()."""

    for syntaxlevel, pattern in SBB_PATTERNS.items():
        match = _re.search(pattern, code)
        if match:
            if syntaxlevel=='nvt':
                return _np.nan
            else:
                return match.group(1).zfill(2)

    for syntaxlevel, pattern in VVN_PATTERNS.items():
        match = _re.search(pattern, code)
        if match:
            if syntaxlevel=='nvt':
                return _np.nan
            else:
                return match.group(2).zfill(2)

    _logger.error(f'No matching syntaxon class found for "{code}".')
    return None


def syntaxonclass(code):
    """Return syntraxonomical class of given staatsbosbeheer catalogus syntaxon code.
    
    Parameters
    ----------
    code : string
        Valid Syntaxon code.

    Returns
    -------
    str or numpy.nan
        class code of syntaxon
    """

    if isinstance(code, _pd.Series):
        synclass = code.apply(_syntaxonclass_string)
        return synclass

    if isinstance(code, list):
        if all(isinstance(item, str) for item in code):
            synclass = [_syntaxonclass_string(x) for x in code]
            return synclass
        else:
            raise ValueError((f'Not all syntaxoncodes are of type '
                f'string: "{code}".'))

    if isinstance(code, str):
        synclass = _syntaxonclass_string(code)
        if not synclass:
            _logger.error(f'No matching pattern found for "{code}"')      
        return synclass

    if _pd.isnull(code):
        _logger.error((f'Input "{code}" of type {type(code)} is no valid '
            f'syntaxon input.'))
        return None

    raise ValueError((f'Unknown type for syntaxon code: {type(code)}'))
    ##return None


def _syntaxonlevel_string(code, reference=None):
    """Return syntaxonomical level of syntaxon 'code'."""

    # get regex patterns
    if reference=='sbbcat':
        PATTERNS = SBB_PATTERNS
    elif reference in ['rvvn','vvn']:
        PATTERNS = VVN_PATTERNS

    # match patterns to code
    for syntaxlevel, pattern in PATTERNS.items():
        if _re.search(pattern, code):
            if syntaxlevel=='nvt':
                return _np.nan
            else:
                return syntaxlevel

    # return None if no match was found
    _logger.error((f'No matching syntaxon level found for "{code}" '
        f'in reference system "{reference}".'))
    return None


def syntaxonlevel(code, reference='sbbcat'):
    """Return syntaxonomic level of given staatsbosbeheer catalogus 
    syntaxon code.
    
    Parameters
    ----------
    code : string
        Valid Staatsbosbeheer syntaxon code.
    reference : {'sbbcat', 'vvn', 'rvvn'}, default 'sbbcat'
        Syntaxonomic reference system.

    Returns
    -------
    str
        syntaxon level
       
    Notes
    -----
    Parameter "reference" defines the syntaxonomical reference system,
    either the "Staatsbosbeheer Catalogus" or the "Vegetatie van Nederland".
    Supplying the reference system is nessecary to distinguish between the
    alliance level in the "Staatsbosbeheer Catalogus" (e.g. "5A" and the 
    order level in the "Vegetatie van Nederland" (e.g. "5A").
              
    """

    if reference not in SUPPORTED_REFERENCE_SYSTEMS:
        raise ValueError(f'Invalid reference system "{reference}".')

    if isinstance(code, _pd.Series):        
        syntaxlevel =  _pd.Categorical(
            values = code.apply(_syntaxonlevel_string, reference=reference),
            categories = SYNTAXON_ORDER,
            ordered=True,
            )
        return syntaxlevel

    elif isinstance(code, str):
        syntaxlevel =  _syntaxonlevel_string(code, reference=reference)
        return syntaxlevel

    elif _pd.isnull(code):
        return _np.nan

    _logger.error((f'Unknown type for syntaxon code: {type(code)}'))
    return None #_np.nan


def syntaxon_codetest(code=None, reference='sbbcat'):
    """Return validated syntaxon, syntaxonomical level and class name
    for a list of synstaxon codes.
    
    Parameters
    ----------
    code : string | list of strings
        Syntaxon code(s) to be tested.
    reference : {'sbbcat', 'vvn'}, default 'sbbcat'
        Syntaxonomical reference system.

    Returns
    -------
    DataFrame
        Table of given sysntaxon codes, validated syntaxon codes,
        syntaxonomcal level and syntaxon class code.

    Notes
    -----
    This function is used to test wether a string is recognised as a 
    valid syntaxon code. In this way, it's possible to test if codes 
    with human typing errors will still be recognised as valid syntaxon 
    codes. When no codes are given, default codes will be used from 
    SBB_TESTCODES or VVN_TESTCODES.
        
    """
    if not code:
        if reference=='sbbcat':
            code = SBB_TESTCODES
        elif reference in ['vvn', 'rvvn']:
            code = VVN_TESTCODES
        else:
            _logger.error(f'Reference system "{reference}" is not supported.')
            return _pd.DataFrame()

    # checking for NaN, numbers and string
    if isinstance(code, float):
        return _np.nan
    if isinstance(code, str):
        code = [code]

    tested = []
    for syncode in code:
        validated = syntaxon_validate(syncode)
        corrected = 'Nee' if syncode==validated else 'Ja'
        level = syntaxonlevel(validated, reference=reference) if validated else None
        synclass = syntaxonclass(syncode)

        tested.append({
            'code' : syncode,
            'validated' : validated,
            'corrected' : corrected,
            'syntaxlevel' : level,
            'syntaxclass' : synclass,
            })

    return _pd.DataFrame(tested)

