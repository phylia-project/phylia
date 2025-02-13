
import os as _os
import numpy as _np
from pandas import Series, DataFrame
import pandas as _pd

def relativepath(abspath, rootdir):
    """Replace absolute path names with paths relative to root
    
    Parameters
    ----------
    abspath : pd.Series | str
        Absolute pathname.

    rootdir : str
        Absolute path to root directory

    Returns
    -------
    pd.Series, str
    
    """
    if isinstance(abspath,Series):

        if not abspath.empty:
            relpath = abspath.apply(lambda x:'..\\'+x.removeprefix(
                rootdir) if not _pd.isnull(x) else x)
        else:
            relpath = abspath.copy()

    elif isinstance(abspath,str):
        relpath = '..\\'+abspath.removeprefix(rootdir)

    else:
        raise ValueError((f'Invalid absolutepath source {abspath}'))

    return relpath



def absolutepath(relpath, rootdir):
    """Replace relative path name with absolute path name.
    
    Parameters
    ----------
    relpath : pd.Series | str
        Relative pathnames.

    rootdir : str
        Absolute path to root directory.

    Returns
    -------
    pd.Series, str
    
    """
    if isinstance(relpath,Series):

        if not abspath.empty:
            abspath = relpath.apply(
                    lambda x:_os.path.join(rootdir,x.lstrip('..\\'))
                    if not _pd.isnull(x) else _np.nan
                    )
        else:
            abspath = relpath.copy()

    elif isinstance(relpath,str):
        abspath = _os.path.join(rootdir,relpath.lstrip('..\\'))

    else:
        raise ValueError((f'Invalid relativepath source {relpath}'))

    return abspath

def is_tv2_complete(dirpath):
    """Return True if folder contains Turboveg2 database files.
    
    Parameters
    ----------
    dirpath : str
        Valid directory path.

    Returns
    -------
    Bool
        
    """

    files = [f for f in _os.listdir(dirpath) if _os.path.isfile(_os.path.join(dirpath, f))]
    has_tvhab = 'tvhabita.dbf' in [f.lower() for f in files]
    has_tvabu = 'tvabund.dbf' in [f.lower() for f in files]
    has_tvrem = 'remarks.dbf' in [f.lower() for f in files]
    has_tvadmin = 'tvadmin.dbf' in [f.lower() for f in files]
    has_tvwin = 'tvwin.dbf' in [f.lower() for f in files]
    
    if (has_tvhab & has_tvabu & has_tvrem & has_tvadmin & has_tvwin):
        is_complete = True
    else:
        is_complete = False

    return is_complete

def is_tv2(dirpath):
    """Return True if folder contains all mandatory Turboveg2 database 
    files.
    
    Parameters
    ----------
    dirpath : str
        Valid directory path.

    Returns
    -------
    Bool
        
    """
    files = [f for f in _os.listdir(dirpath) if _os.path.isfile(_os.path.join(dirpath, f))]
    has_tvhab = 'tvhabita.dbf' in [f.lower() for f in files]
    has_tvabu = 'tvabund.dbf' in [f.lower() for f in files]
    has_tvrem = 'remarks.dbf' in [f.lower() for f in files]

    if (has_tvhab | has_tvabu | has_tvrem):
        is_tv2folder = True
    else:
        is_tv2folder = False

    return is_tv2folder
