
import pytest
import os
from pandas import Series
import pandas as pd
import numpy as np

from phylia.tools.sbbprojects import SbbProjects
import phylia

root = r'.\data\sbbprojects\\'

def class_sbbprojects(root=root):
    """Test creating SbbProjects instance"""

    sbbprj = SbbProjects(root)
    assert isinstance(sbbprj, phylia.SbbProjects)
    assert len(sbbprj)>0
    assert isinstance(str(sbbprj), str)


def count_projectfiles():
    pass


def get_filetype(root=root):

    sbbprj = SbbProjects(root)
    df = sbbprj.get_allfiles()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def get_mdbfiles(root=root):
    
    sbbprj = SbbProjects(root)
    df1, df2 = sbbprj.get_mdbfiles()

    assert not df1.empty
    assert isinstance(df2, pd.DataFrame)


def get_projectfiles():
    pass


def get_projectfolders(root=root):

    sbbprj = SbbProjects(root)

    df = sbbprj.get_projectfolders(relpaths=True)
    assert isinstance(df, pd.Series)
    assert not df.empty

    df = sbbprj.get_projectfolders(relpaths=False)
    assert isinstance(df, pd.Series)
    assert not df.empty


def get_rootfolder(root=root):

    sbbprj = SbbProjects(root)
    assert os.path.isdir(sbbprj.get_rootfolder())


def get_shapefiles(root=root):

    sbbprj = SbbProjects(root)
    df1, df2 = sbbprj.get_shapefiles()

    assert not df1.empty
    assert isinstance(df2, pd.DataFrame)


def get_tv2ambiguous():
    pass


def get_tv2duplicates():
    pass


def get_tv2folders():

    sr = sbbprj.get_tv2folders()
    assert isinstance(sr, Series)
    assert not sr.empty


def split_projectnames(root=root):

    sbbprj = SbbProjects(root)
    df = sbbprj.split_projectnames()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty





