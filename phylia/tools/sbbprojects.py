import re as _re
import os as _os

import numpy as _np
##from pandas import Series, DataFrame
import pandas as _pd
##import difflib

from . import filetools as _filetools
#from .filetools import relativepath as _relativepath, 
#from .filetools import absolutepath as _absolutepath
##from . import conversions as _conversions ##import year_from_string as _year_from_string

import logging as _logging
#from logging import getLogger
_logger = _logging.getLogger(__name__)


class SbbProjects:
    """
    Find filepaths to ESRI shapefiles and Microsoft Acces database files 
    for each projectfolder under a given root directory.

    The method list_projectfiles() returns a table with all projects 
    and the corresponding shapefile and access mdbfile, if they were 
    found. This table is the main result for this class, all the other 
    methods are merely preparations and checks.

    Methods
    -------
    get_projectfiles
        Return table with all projects and filepaths found.
    get_projectfolders
        Return table of project directories under root.
    get_filetype
        Return table with all files of given filetype under root.
    get_mdbfiles
        Return table with project mdbfiles.
    get_shapefiles
        Return table with project shapefiles.

    get_rootfolder
        Return the name of the root folder.
    split_projectnames
        Return table of seperate elements of project folder name.

    list_tv2
        Return table with all Turboveg2 project files
        under a project folder.
    count_projectfiles
        Return table of file counts by project for given filtetype.

    Notes
    -----
    Projects are supposed to be organised in subfolders under a root 
    folder. Projectfolders should be at the second level beneath the 
    root folder. 
    The first level beneath the root folder is called 'provincie'. 
    A typical project folder path should look like:
    '..\\01_Standaard\Drenthe\Dr 0007_Hijken_1989' 
    where '..\\01_Standaard\' is the root folder.
        
    """

    DEFAULT_DISCARDTAGS = ['conversion','ConversionPGB','catl','ctl','soorten',
        'kopie','test','oude versie','db1','test','fout', 'copy',
        'themas','florakartering','flora','toestand','backup',
        'foutmelding','Geodatabase',]

    INDEXCOL1 = 'provincie'
    INDEXCOL2 = 'project'

    def __init__(self, root, relpaths=True):
        """
        Parameters
        ----------
        root : str
            Root directory above project directories.
        repaths : boolean, default True
            Return relative filepaths.
        """
        if not isinstance(root, str):
            raise TypeError((f'root must be of type string '
                f'not {type(root)}'))

        if not _os.path.isdir(root):
            raise ValueError(f'{root} is not a valid directory name.')

        self._root = root
        self._projects = self._projectfolders(self._root)


    def __repr__(self):
        if self._projects.empty:
            self._projects = self.get_projectfolders()
        ##root = _os.path.basename(_os.path.normpath(self._root))
        ##return (f'{root} ({len(self)} projects)')
        return (f'{len(self)} mapping projects')


    def __len__(self):
        if self._projects.empty:
            self._projects = self.get_projectfolders()
        return len(self._projects)


    def _projectfolders(self, root):
        """Return table of project folders under root folder.
        
        Called by class constructor to create projects table only once.
        """

        prvlist = []    #'Drenthe'
        prjlist = []    #'Dr 0007_Hijken_1989'
        pathlist = []   #fullpath

        prvnames = ([subdir for subdir in _os.listdir(root)
            if _os.path.isdir(_os.path.join(root,subdir))])

        for prvname in prvnames:

            # project names from folder names
            prjnames = [prjdir for prjdir in _os.listdir(
                _os.path.join(root, prvname)) if _os.path.isdir(
                _os.path.join(root, prvname, prjdir))] 
            prjpaths = [_os.path.join(root, prvname, prj) for prj in prjnames]

            # append lists to lists
            prvlist += [prvname]*len(prjnames)
            prjlist += prjnames
            pathlist += prjpaths

        projects = _pd.DataFrame(data=list(zip(prvlist, prjlist, pathlist)),
            columns=[self.INDEXCOL1, self.INDEXCOL2, 'prjdir'])
        projects = projects.set_index(keys=[self.INDEXCOL1, self.INDEXCOL2],
            verify_integrity=True).squeeze()
        
        return projects


    def get_rootfolder(self):
        """Return root folder for mapping folders."""
        return self._root


    def get_projectfolders(self, relpaths=True):
        """Return table of project folders under root folder.

        Parameters
        ----------
        relpaths : bool, default True
            Return pathnames relative to root folder.

        Returns
        -------
        DataFrame

        Notes
        -----
        Staatsbosbeheer vegetation mapping projects are stored in a 
        folder structure below the root folder "..\\01_Standaard\"
        The folder tree has two levels and looks like:
         ..\\01_Standaard\Drenthe\Dr 0007_Hijken_1989
        The first level are Dutch provinces (e.g. 'Drenthe'), 
        the second level are project directories 
        (e.g. "Dr 0007_Hijken_1989"). Folder names at level 2 under 
        the root folder are used as Projectnames.

        Mapping projects that cross province boundaries can be present
        as a project in both provinces. Therefore, grouping must be done
        on the combination of "province" and "project".
           
        """
        projects = self._projects
        if relpaths:
            projects = _filetools.relativepath(projects, rootdir=self._root)
        return projects


    def _validate_filetype(self,filetype=None):
        """Return valid filetype string or None"""
        if filetype is not None:
            if isinstance(filetype,str):
                filetype=filetype.lstrip('.')
                if not len(filetype)==3:
                        warnings.warn(f'{filetype} is not a valid filetype.')
                        filetype=None
            else:
                _logger.warning(f'{filetype} is not a valid filetype.')
                filetype=None
        return filetype


    def _file_in_projectdir(self, filetbl, pathcol=None):
        """
        Return boolean mask for files located in the project folder.

        Parameters
        ----------
        filetbl : pd.DataFrame
            table with filepathnames as returned by list_files()
        pathcol : str
            column name with filepath
            
        """
        prjtbl = self.get_projectfolders()
        prjdirs = _pd.Series(index=filetbl.index,dtype='object')
        for idx in prjdirs.index:
            prv = filetbl.loc[idx,self.INDEXCOL1]
            prj = filetbl.loc[idx,self.INDEXCOL2]
            prjdirs.loc[idx] = prjtbl.loc[(prv,prj)]
        filedirs = filetbl[pathcol].apply(lambda x:_os.path.dirname(x))
        mask = filedirs==prjdirs
        return mask

    def get_filetype(self, filetype=None, relpaths=True):
        """
        Return table of all files under the rootfolder aggregated by 
        project.

        Parameters
        ----------
        filetype : str, optional
            Return only files of type filetype.
        relpaths : bool, default True
            Return paths relative to root folder.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Projects with no files of given filetype will not be present in
        the table that is returned.   
           
        """
        filetype = self._validate_filetype(filetype)
        if filetype is None:
            _logger.warning(f'Filetype is None. All files wil be listed.')

        fpathcol='fpath'
        fnamecol='fname'
        if isinstance(filetype, str):
            fpathcol=f'{filetype}path'
            fnamecol=f'{filetype}name'

        prjtbl = self._projects

        # create list of dicts for each file under a project directory
        # and create dataframe with all filepaths by provincie, project
        pathlist = []
        empty_projects = []
        for (prv,prj), path in prjtbl.items():
            for prjdir, subdirs, files in _os.walk(path):
                for f in files:
                    filepath = _os.path.join(prjdir,f)
                    rec = {
                        self.INDEXCOL1 : prv,
                        self.INDEXCOL2 : prj,
                        f'{fpathcol}' : str(filepath),
                        f'{fnamecol}' : f,
                        }
                    pathlist.append(rec.copy())
        tbl = _pd.DataFrame(pathlist)

        # reorder columns
        colnames = [self.INDEXCOL1,self.INDEXCOL2]+[fnamecol,fpathcol]
        tbl = tbl[colnames]

        if filetype is not None:
            mask = tbl[fpathcol].str.endswith(f'.{filetype}')
            tbl = tbl[mask].copy()

        if relpaths: #remove root from paths
            tbl[fpathcol] = _filetools.relativepath(tbl[fpathcol], rootdir=self._root)

        return tbl.reset_index(drop=True)


    def count_projectfiles(self, colname=None, 
        fill_missing=True):
        """
        Return table of filecounts by project for given filtetype

        Parameters
        ----------
        colname : str, optional
            Give filecounts only for this column.
        fill_missing : bool, default True
            Include projects with zero files.

        Returns
        -------
        pd.DataFrame

        """
        filetbl = self.get_projectfiles()

        """
        if not isinstance(filetbl,_pd.DataFrame):
            logger.error(f'{filetbl} is not a DataFrame')
            return DataFrame()
        if colname is None:
            colname = 'shpname'
        """
        if isinstance(colname, str): 
            if colname not in filetbl.columns:
                _logger.error((f'"{colname}" not in filetbl columns: '
                    f'{list(filetbl)}. Counts for all columns will be '
                    f'returned.'))
                colname = None

        grp = filetbl.groupby(by=[self.INDEXCOL1, self.INDEXCOL2])
        filecounts = grp.count()
        if colname is not None:
            filecounts = filecounts[colname].copy()
            filecounts.name = f'{colname}_counts'

        if fill_missing:
            index = self.get_projectfolders().index
            filecounts = filecounts.reindex(index=index,fill_value=0)

        return filecounts


    def _ambiguous_filepaths(self, masktbl):
        """
        Return table of all filenames for projects where no single 
        projectfile could be identified with certainty.
        
        Parameters
        ----------
        masktbl : pd.DataFrame
            Boolean values for filtering.

        Returns
        -------
        pd.DataFrame
            
        """
        tblist = []

        # group all files by project. If any file is marked 'masksel'
        # then this file is the wanted projectfile. If no such file
        # is present, return a table with all filenames in a project
        # and let the user sort it all out.
        for (provincie,project),tbl in masktbl.groupby([self.INDEXCOL1,self.INDEXCOL2]):
            any_masksel = tbl['masksel'].any()
            if 'likename' in list(tbl):
                any_likename = tbl['likename'].any()
            else:
                any_likename = True
            if (not any_masksel) and any_likename:
                tblist.append(tbl)

        if tblist: #return table of ambigous filenames
            ambiguous = _pd.concat(tblist)
            _logger.info(f'{len(ambiguous)} filepaths names with ambiguous status have been found.')
        else: #return empty dataframe
            ambiguous = _pd.DataFrame(columns=masktbl.columns)

        return ambiguous


    def get_mdbfiles(self, use_discard_tags=False, taglist=None,
        priority_filepaths=None):
        """
        Return table with mdbfiles by project and table with projects 
        for which no single mdb-file could be selected.

        Parameters
        ----------
        use_discard_tags : bool, default False
            Use default list of tags to discard projectfolders with 
            names that indicate copies or discarded data. The list
            of default tags is named DEFAULT_DISCARD_TAGS.
        taglist : list of strings
            Folders with these words in their folderpath will be 
            discarded as possible projectfolders. Value of 
            use_discard_tags will be ignored if a list is given.
        priority_filepaths : list of string, optional
            Mdb filepaths in this list are selected as projectfiles.
            Other candidate projectfiles will be ignored.

        Returns
        -------
        mdbsel : DataFrame
            Table with selected mdbfiles.
        ambiguous : DataFrame
            Table with projects for which multiple mdbfiles remain
            present after filtering.

        Notes
        -----
        The result "mdbsel" includes only projects for which exactly 
        one mdb file could be identified as the most likely project 
        file. 
        Projects with multiple possible mdbfiles are listed in the 
        table "ambiguous".

        Valid mdb projectfiles can have any filename. Selection is based
        on file location (files high in the project folder structure have 
        priority).
        Filepaths that contain words present in use_discard_tags 
        will be discarded. 
        Filepaths equal to strings in "priority_filepaths" are selected 
        when multiple files are present.
            
        """
        filetbl = self.get_filetype(filetype='mdb', relpaths=True)

        if use_discard_tags:
            discard_tags = self.DEFAULT_DISCARDTAGS
        else:
            discard_tags = []

        if taglist:
            if not isinstance(taglist, list):
                _logger.error(f'Input argument pathtags with invalid '
                    f'value {discard_tags} will be ignored.')
                discard_tags = self.DEFAULT_DISCARDTAGS

        # mask for mdbfile in project directory
        mask_prjdir = self._file_in_projectdir(filetbl, pathcol='mdbpath')

        # mask for tags in pathfilter
        if discard_tags:
            ##lowertags = [x.lower() for x in use_discard_tags]
            ##mask_fpath = filetbl['mdbpath'].str.lower().str.contains(
            ##    '|'.join(lowertags),na=False,regex=True,case=False)
            ##mask_fpath = filetbl['mdbpath'].str.contains(
            ##    '|'.join(use_discard_tags),na=False,regex=True,case=False)
            mask_fpath = filetbl['mdbpath'].apply(
                lambda x: any([tag.lower() in str(x).lower() for tag in discard_tags]))
            
            sumfpath = sum(mask_fpath)
            _logger.warning((f'{sumfpath} rows with mdb-files have been '
                f'marked as copies based on given tags.'))
        else:
            mask_fpath = _pd.Series(data=False,index=filetbl.index)


        # masktbl is a temporary copy of filetbl with columns for masking
        # mask_fname and mask_prjdir are series with the same index
        # as DataFrame filetbl.
        masktbl = filetbl.copy()
        masktbl['maskprj'] = mask_prjdir
        masktbl['maskfpath'] = ~mask_fpath
        masktbl['masksel'] = False

        # step-wise select most probable mdb projectfile
        for (provincie, project), tbl in masktbl.groupby([self.INDEXCOL1, self.INDEXCOL2]):

            if len(tbl)==1:
                # just one mdb in entire project tree structure
                idx = tbl.index[0]
            elif len(tbl[tbl['maskprj']])==1:
                # exactly one mdb in prjdir
                idx = tbl[tbl['maskprj']].index[0]
            elif len(tbl[tbl['maskfpath']])==1:
                # only one mdbfile found in entire tree structure 
                # after excluding unlikely files
                idx = tbl[tbl['maskfpath']].index[0]
            elif len(tbl[tbl['maskprj']&tbl['maskfpath']])==1:
                # only one mdb in prjdir after discarding unlikely 
                # files by pathname
                idx = tbl[tbl['maskprj']&tbl['maskfpath']].index[0]
            else:
                idx = None

            if (not idx) and priority_filepaths:
            # At this point, idx is still None. An mdb-projectfile has
            # not been choosen based on automated selection.
            # Parameter priority_filepaths contains a list of filepaths
            # of mdb-projects. If any of these filepaths is present in 
            # column mdbpath, this file will be selected.
                mask = tbl['mdbpath'].isin(priority_filepaths)
                if len(tbl[mask])==1:
                    idx = tbl[mask].index[0]

            if idx is not None:
                # mark chosen file as selected
                masktbl.loc[idx,'masksel']=True

        # create table of projects with selected mdb files
        mdbsel = filetbl[masktbl['masksel']]

        # create table of projects with to many ambiguous files to 
        # select a project mdb file
        ambiguous = self._ambiguous_filepaths(masktbl)

        return mdbsel, ambiguous


    def get_shapefiles(self, shapetype='polygon', priority_filepaths=None, 
        column_prefix=None,):
        """
        Return table with project shapefiles and table with possible 
        projectfiles for projects where no single projectfile could be 
        identified with certainty.

        Parameters
        ----------
        shapetype : {'polygon','line'}, default 'polygon'
            Type of shapefile to filter.
        column_prefix : str, optional
            Column in filetbl with filename. If None, default name is
            inferred from value of shptype.
        priority_filepaths : list of strings, optional
            Filepaths equal to a string in this list will allways be 
            selected as project shapefile, discarding other files.

        Returns
        -------
        shapesel : pd.DataFrame
            Table with selected shapefiles.
        ambigous : pd.DataFrame
            Table with shapefiles for projects for which no single 
            shapefile could be selected.

        Notes
        -----
        - Valid shapefiles with vegetation polygons are called 'vlakken', 
          'Vlakken', or they have the keyword 'vlak' somewhere in their 
          filename. 
        - For line elements these keywords are 'lijnen' or 'lijn'. 
        - For point elements keyword is 'point'.
            
        """
        # TODO: Add functionality for ignoring filepaths with names that
        # indicate folders that have been copied or discarded (like in 
        # get_mdbfiles()

        filetbl = self.get_filetype(filetype='shp', relpaths=True)

        # masks for filename contains keyword
        if shapetype=='polygon':
            key_isname = 'vlakken.shp'
            key_contains = 'vlak'
            if column_prefix is None:
                column_prefix = 'poly'
        elif shapetype=='line':
            key_isname = 'lijnen.shp'
            key_contains = 'lijn'
            if column_prefix is None:
                column_prefix = 'line'
        else:
            raise(f'{shapetype} is not a valid shapefile type. ')

        namecol='shpname'
        pathcol='shppath'

        isname = filetbl[namecol].str.lower()==key_isname
        likename = filetbl[namecol].str.lower().str.contains(key_contains)

        # mask for file in project directory
        masktbl = filetbl.copy()
        mask_prjdir = self._file_in_projectdir(masktbl,pathcol=pathcol)

        # masktbl is a temporary copy of filetbl with columns for masking
        # mask_fname and mask_prjdir are series with the same index
        # as DataFrame filetbl.
        masktbl['isname'] = isname
        masktbl['likename'] = likename
        masktbl['inprj'] = mask_prjdir
        masktbl['masksel'] = False


        # step-wise select most probable shp projectfile
        for (provincie,project),tbl in masktbl.groupby([self.INDEXCOL1,self.INDEXCOL2]):

            if len(tbl[tbl['isname']])==1: 
                # only one file named 'vlakken'
                idx = tbl[tbl['isname']].index[0]
            elif len(tbl[tbl['isname']&tbl['inprj']])==1:
                # only one file vlakken in projectfolder
                idx = tbl[tbl['isname']&tbl['inprj']].index[0]
            elif len(tbl[tbl['likename']])==1:
                # only one file with name like vlakken
                idx = tbl[tbl['likename']].index[0]
            elif len(tbl[tbl['likename']&tbl['inprj']])==1:
                # only one file with name like vlakken in projectfolder
                idx = tbl[tbl['likename']&tbl['inprj']].index[0]
            else:
                idx = None

            if (not idx) and priority_filepaths:
            # At this point, idx is still None. No shp-projectfile has
            # been choosen based on automated selection.
            # Parameter shpfilepaths contains a list of filepaths of 
            # shapefiles. If any of these filepaths is present in 
            # column shppath, this file will be selected.
                mask = tbl[pathcol].isin(priority_filepaths)
                if len(tbl[mask])==1:
                    idx = tbl[mask].index[0]

            if idx is not None:
                masktbl.loc[idx,'masksel']=True

        self._shpfilter = masktbl

        # rename columns in table
        if column_prefix is not None:
            filetbl = filetbl.rename(columns={
                'shpname': f'{column_prefix}name',
                'shppath': f'{column_prefix}path',
                })

        # create table of projects with selected project files
        shpsel = filetbl[masktbl['masksel']].reset_index(drop=True)
        shpsel = shpsel.sort_values(by=[self.INDEXCOL1,self.INDEXCOL2])

        # create table of projects with to many ambiguous files to 
        # select a project file
        ambiguous = self._ambiguous_filepaths(masktbl).reset_index(drop=True)
        ambiguous = ambiguous.sort_values(by=[self.INDEXCOL1,self.INDEXCOL2])

        return shpsel, ambiguous


    def get_tv2(self, relpaths=True):
        """
        Return table of projects and the path to the Turboveg2 data folder.

        Parameters
        ----------
        relpaths : bool, default True
            Return directory paths relative to root folder.

        Returns
        -------
        Series

        Notes
        -----
        A table with all projectfolders is returned. When at least one 
        folder with TV2 database files is found below a projectfolder, 
        the path tot this folder is filled in when:
        1. There is only one folder with TV2 files under the project 
           folder.
        2. There is one TV2 folder that is hogher in the project tree 
           than all other folders with TV2 files.
        When no folder with TV2 files is present or when multiple 
        possible folders remain, the path tot the TV2 folder is left 
        empty.
            
        """

        # selected tvfolders to series
        tvdir = self.get_tv2folders(relpaths=relpaths, include='selected')
        tvdir = tvdir.set_index([self.INDEXCOL1,self.INDEXCOL2], 
            verify_integrity=True)

        # merge with projects table
        prjtbl = self.get_projectfolders()
        tvdir = _pd.merge(prjtbl,tvdir, left_index=True, right_index=True, 
            how='left').squeeze()

        return tvdir


    def get_tv2folders(self, include='all', relpaths=True):
        """Return names of folders with TV2 files.

        Parameters
        ----------
        include : {'selected', 'ambiguous', 'duplicates', 'all'}, default 'all'
            selected : only folders with a TV2 dataset that has been 
                selected as best data source for a project are returned.
            ambiguous : all folders for projects where selection of a 
                best possible tv2 datasource was not possible are returned.
            duplicates : all folders for projects with more than one 
                tv2 dataset are returned.
            all : all folders with a tv2 dataset are returned.
        relpaths : bool, default True
            Return directory paths relative to root folder.

        Returns
        -------
        pandas DataFrame
            
            
        """

        # list of selected tv2folders
        tvdir = self._tv2_mark_selected_folders()

        if include=='selected':

            selected = tvdir['selected']==True
            tvdir = tvdir[selected]


        elif include=='duplicates':

            mask1 = tvdir['criterion']!='single directory'
            mask2 = tvdir.duplicated(subset=['provincie','project'], keep=False)
            tvdir = tvdir[mask1&mask2].copy()


        elif include=='ambiguous':

            mask1 = tvdir['selected']==False
            mask2 = tvdir['rejected']==False
            tvdir = tvdir[mask1&mask2].copy()

        elif include=='all':
            pass

        else:
            raise ValueError(f'Invalid value "{include}".')

        if relpaths: #remove root from paths
            tvdir['tvdir'] = _filetools.relativepath(tvdir['tvdir'], 
                rootdir=self.get_rootfolder())
            
        return tvdir

    
    def get_tv2duplicates(self, relpaths=True):
        """Return path names for all Turboveg2 databases in projects with 
        multiple databases (includes projects where a single database could
        be selected).

        Parameters
        ----------
        relpaths : bool, default True
            Return directory paths relative to root folder.

        Returns
        -------
        pandas DataFrame
        
        """

        # table of projects with multiple tv2 databases
        tvdir = self._tv2_mark_selected_folders()
        mask1 = tvdir['criterion']!='single directory'
        mask2 = tvdir.duplicated(subset=['provincie','project'], keep=False)
        tvdir = tvdir[mask1&mask2].copy()

        if relpaths: #remove root from paths
            tvdir['tvdir'] = _filetools.relativepath(tvdir['tvdir'], 
                rootdir=self.get_rootfolder())

        return tvdir


    def get_tv2ambiguous(self, relpaths=True):
        """Return turboveg2 folder names for projects where no single folder could be selected.

        Parameters
        ----------
        relpaths : bool, default True
            Return directory paths relative to root folder.

        Returns
        -------
        pandas DataFrame
        
        """
        tvdir = self._tv2_mark_selected_folders()
        mask1 = tvdir['selected']==False
        mask2 = tvdir['rejected']==False
        tvdir = tvdir[mask1&mask2].copy()

        if relpaths: #remove root from paths
            tvdir['tvdir'] = _filetools.relativepath(abspath=tvdir['tvdir'], 
                rootdir=self.get_rootfolder())

        return tvdir


    def _tv2_find_all_folders(self):
        """Return table with directory paths for all drectories with 
        Turboveg2 project files under root.
        
        Notes
        -----
        The criterium for being a Turboveg2 project folder is the 
        presence of a file called 'tvhabita.dbf'.
        """

        # finding all turboveg2 folders takes a lot of time
        # this is done only once for an object
        if '_tv2folders' in self.__dict__.keys():
            return self._tv2folders

        # get table of project directories
        prjtbl = self._projects

        # traverse from root through all project directories and 
        # subdirectories and find all directories with Tuboveg2 files
        tvdirs=[]
        for (prv,prj), dirpath in prjtbl.items():


            for filedir, subdirs, files in _os.walk(dirpath):

                tvhab = 'tvhabita.dbf' in [f.lower() for f in files]
                tvabu = 'tvabund.dbf' in [f.lower() for f in files]
                tvrem = 'remarks.dbf' in [f.lower() for f in files]

                if tvhab|tvabu|tvrem: # any turboveg file present
                    rec = {
                        self.INDEXCOL1:prv, 
                        self.INDEXCOL2:prj, 
                        'tvdir':filedir
                        }

                    tvdirs.append(rec.copy())

        self._tv2folders = _pd.DataFrame(tvdirs)
        return self._tv2folders


    def _tv2_mark_selected_folders(self):
        """Return table of TV2 folders and best directory. """

        # get all tv2 folders under root
        tvdir = self._tv2_find_all_folders()

        tvdir['path_depth'] = tvdir['tvdir'].apply(
            lambda x:len(_os.path.normpath(x).split(_os.sep)))

        # default start values
        # in the foloo
        tvdir['selected']=False
        tvdir['rejected']=False
        tvdir['criterion'] = 'ambiguous'

        for (prv,prj), tbl in tvdir.groupby(by=[self.INDEXCOL1,self.INDEXCOL2]):

            # mask for directories at the highest level in the tree
            is_highest_level = tbl['path_depth']==tbl['path_depth'].min()

            # mark best directories as selected and the others as rejected
            if len(tbl)==1: 
                # easy: just one tv2 directory
                icol = tbl.columns.get_loc('tvdir')
                seldir = tbl.iloc[0,icol]
                criterion = 'single directory'

                """
                elif len(tbl[tbl['mask_tv']])==1:
                    # select directories starting with _TV

                    # get name of selected directory
                    icol = tbl.columns.get_loc('tvdir')
                    seldir = tbl[tbl['mask_tv']].iloc[0,icol]

                elif len(tbl[tbl['mask_tv']&~tbl['mask_tag']])==1:
                    # just one directory after discarding directories with
                    # specific tags in pathname

                    # get name of selected directory
                    icol = tbl.columns.get_loc('tvdir')
                    seldir = tbl[tbl['mask_tv']&~tbl['mask_tag']].iloc[0,icol]
                """
            elif len(tbl[is_highest_level])==1:
                # a single one directory is on the highest level in the tree
                icol = tbl.columns.get_loc('tvdir')
                seldir = tbl[is_highest_level].iloc[0,icol]
                criterion = 'upper directory'

            else:
                # no "best" directory has been found
                continue

                _logger.warning((f'No single best directory with Turboveg '
                    f'files found for {prv} {prj}.'))

            # mark alll records of current project as rejected
            tvdir.loc[tbl.index.values,'rejected'] = True
            tvdir.loc[tbl.index.values,'criterion'] = criterion

            # mark only selected project as not rejected
            idx_selected = tvdir[tvdir['tvdir']==seldir].index.values[0]
            tvdir.loc[idx_selected,'rejected']=False
            tvdir.loc[idx_selected,'selected']=True

        return tvdir


    def get_projectfiles(self, relpaths=True, use_discard_tags=False, 
        taglist=None, mdbpaths=None, polygonpaths=None,
        linepaths=None, pointpaths=None):
        """
        Return table with all projects and filepaths found

        Parameters
        ----------
        relpaths : bool, default True
            Filepaths relative to root directory.

        use_discard_tags : bool, default True
            Use default list of tags to discard projectfolders with 
            names that indicate copies or discarded data. The list
            of default tags is named DEFAULT_DISCARD_TAGS.
        taglist : list of strings
            Folders with these words in their folderpath will be 
            discarded as possible projectfolders. Value of 
            use_discard_tags will be ignored if a list is given.
        mdbpaths : list of string, optional
            Filepaths in this list will be selected as projectfiles.
            Other project filepaths will be ignored.
        polygonpaths : list of strings, optional
            Filepaths in this list will be selected as projectfiles.
            Other project filepaths will be ignored.
        linepaths : list of strings, optional
            Filepaths in this list will be selected as projectfiles.
            Other project filepaths will be ignored.
        pointpaths : list of strings, optional
            Filepaths in this list will be selected as projectfiles.
            Other project filepaths will be ignored.
           
        """

        if use_discard_tags:
            discardtags = self.DEFAULT_DISCARDTAGS
        else:
            discardtags = []

        if taglist:
            discardtags = taglist

        # find mdb files
        #mdblist = self.get_filetype(filetype='mdb')
        mdbsel, ambigous = self.get_mdbfiles( 
            use_discard_tags=use_discard_tags,
            taglist=discardtags, 
            priority_filepaths=mdbpaths
            )
        mdbsel = mdbsel.set_index(keys=[self.INDEXCOL1,self.INDEXCOL2],
            verify_integrity=True)

        ambiprj = len(set(ambigous[self.INDEXCOL2].values))
        if ambiprj!=0:
            _logger.warning((f'{ambiprj} projects with multiple mdb-files '
                f'have been dropped from projectstable. Use '
                f'method get_mdbfiles to get a table of candidate '
                f'files.'))

        # table of all available shapefiles
        ##shp = self.list_allfiles(filetype='shp')
        
        # find polygon shapefiles
        polysel, ambigous = self.get_shapefiles(shapetype='polygon',
            priority_filepaths=polygonpaths)
        polysel = polysel.set_index(
                keys=[self.INDEXCOL1,self.INDEXCOL2],verify_integrity=True)

        ambiprj = len(set(ambigous[self.INDEXCOL2].values))
        if ambiprj!=0:
            _logger.warning((f'{ambiprj} projects with multiple polygonfiles '
                f'have been dropped from projectstable. Use '
                f'method filter_shpfiles to get a table of candidate '
                f'files.'))

        # find line shapefiles
        linesel,ambigous = self.get_shapefiles(shapetype='line',
            priority_filepaths=linepaths)
        linesel = linesel.set_index(
                keys=[self.INDEXCOL1, self.INDEXCOL2], verify_integrity=True)

        ambiprj = len(set(ambigous[self.INDEXCOL2].values))
        if ambiprj!=0:
            _logger.warning((f'{ambiprj} projects with multiple linefiles '
                f'have been dropped from projectstable. Use '
                f'method filter_shpfiles to get a table of candidate '
                f'files.'))

        # list of TV2 directories
        #tvambi = self.get_tv2ambiguous()
        #if not tvambi.empty:
        #    _logger.warning((f'{ambiprj} projects with multiple TV2 directories '
        #        f'found. Call get_tv2ambiguous '
        #        f'to get a table of ambiguous '
        #        f'files.'))

        ##tvsel = tvdir[tvdir['selected']==True].set_index([self.INDEXCOL1,self.INDEXCOL2])
        ##tvsel = tvsel[['tvdir']].copy()
        ##if relpaths: #remove root from paths
        ##    tvsel['tvdir'] = _filetools.relativepath(tvsel['tvdir'], rootdir=self.get_rootfolder())
        tvsel = self.get_tv2(relpaths=True)

        # merge file tables with base project table
        ##baseprj = self.get_projectfolders()
        ##baseprj = baseprj[['year']].copy()
        baseprj = self.split_projectnames()['year'].to_frame()

        prj = _pd.merge(baseprj,mdbsel,left_index=True,right_index=True,
            how='left',suffixes=[None,'_from_mdb'],validate='one_to_one')
        prj = _pd.merge(prj,polysel,left_index=True,right_index=True,
            how='left',suffixes=[None,'_from_poly'],validate='one_to_one')
        prj = _pd.merge(prj,linesel,left_index=True,right_index=True,
            how='left',suffixes=[None,'_from_line'],validate='one_to_one')
        prj = _pd.merge(prj,tvsel,left_index=True,right_index=True,
            how='left',suffixes=[None,'_from_tv2'],validate='one_to_one')

        # drop duplicaste columns names
        colnames = []
        for tag in ['_from_mdb','_from_poly','_from_line','_from_tv2',]:
            colnames = colnames + [x for x in prj.columns if tag in x]
        prj = prj.drop(columns=colnames)

        # relative paths or absolute paths
        if not relpaths:
            pathcols = [x for x in prj.columns if 'path' in x]
            for col in pathcols:
                prj[col]=_filetools.absolutepath(prj[col], rootdir=self.get_rootfolder())

        return prj


    def split_projectnames(self):
        """Return table with seperate elements of projectnames 
        (project code, project name, project year).

        The names of mapping projects in de Staatsbosbeheer folder
        structure are composed of several elements that contain 
        information about the project (number, name and year). 
        Unfortunately, not all follders have been named consistently,
        but this function tries to retrieve the sepereate element for 
        each folder.
        The column "match" gives information about the regular 
        expression that matched the specific folder name. Rows without 
        a match have the value NaN.
            
        """

        # split folder names in seperate elements
        df = _pd.DataFrame(self.get_projectfolders(relpaths=True))
        df['prjcode'] = df.index.get_level_values(1)
        df['prjname'] = df.index.get_level_values(1)
        df['year'] = df.index.get_level_values(1)
        df['match'] = df.index.get_level_values(1)
        df = df[['prjcode','prjname','year','match']].copy()

        # try to match elements to information using regular expressions
        patterns = [
            r'^[A-Za-z]{2,3}[ _](\d{3,4})[ _](.*)[ _](\d{4}$)', # prv (prjcode) (naam) (jaar)
            r'^[A-Za-z]{2,3}[ _]()(.*)[ _](\d{4}$)', # prv (empty) (naam) (jaar)
            r'^(\d{3,6})[ _](.*)[ _](\d{4}$)', # (prjcode) (naam) (jaar)
            r'^(\d{3,4})[ _](.*)()$', # (prjcode) (naam) (empty)
            r'^()(.*)[ _](\d{4}$)', # (empty) (naam) (jaar)
            ]

        for i, pattern in enumerate(patterns):
            df['prjcode'] = df['prjcode'].apply(
                lambda x: _re.search(pattern, x).group(1) if _re.search(pattern, x) else x)
            df['prjname'] = df['prjname'].apply(
                lambda x: _re.search(pattern, x).group(2) if _re.search(pattern, x) else x)
            df['year'] = df['year'].apply(
                lambda x: _re.search(pattern, x).group(3) if _re.search(pattern, x) else x)
            df['match'] = df['match'].apply(
                lambda x: f'pat_{str(i)}' if _re.search(pattern, x) else x)

        # mark rows without match
        df.loc[~df['match'].str.startswith('pat_'),'match']=_np.nan

        return df
