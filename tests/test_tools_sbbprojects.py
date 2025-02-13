
import pytest
import os
from pandas import Series
import pandas as pd
import numpy as np

from phylia.tools.sbbprojects import SbbProjects
import phylia

root = r'.\data\sbbprojects\\'


def test_class_sbbprojects(root=root):
    # Test creating SbbProjects instance

    sbbprj = SbbProjects(root)
    assert isinstance(sbbprj, phylia.SbbProjects)
    assert len(sbbprj)>0
    assert isinstance(str(sbbprj), str)


def test_count_projectfiles(root=root):

    sbbprj = SbbProjects(root)

    df = sbbprj.count_projectfiles()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    sr = sbbprj.count_projectfiles('tvdir')
    assert isinstance(sr, pd.Series)
    assert not sr.empty
    

def test_get_filetype(root=root):

    sbbprj = SbbProjects(root)
    df = sbbprj.get_filetype()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_get_mdbfiles(root=root):
    
    sbbprj = SbbProjects(root)
    df1, df2 = sbbprj.get_mdbfiles()
    assert not df1.empty
    assert isinstance(df2, pd.DataFrame)


def test_get_projectfiles(root=root):

    sbbprj = SbbProjects(root)
    df = sbbprj.get_projectfiles()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_get_projectfolders(root=root):

    sbbprj = SbbProjects(root)

    df = sbbprj.get_projectfolders(relpaths=True)
    assert isinstance(df, pd.Series)
    assert not df.empty

    df = sbbprj.get_projectfolders(relpaths=False)
    assert isinstance(df, pd.Series)
    assert not df.empty


def test_get_rootfolder(root=root):

    sbbprj = SbbProjects(root)
    assert os.path.isdir(sbbprj.get_rootfolder())


def test_get_shapefiles(root=root):

    sbbprj = SbbProjects(root)
    df1, df2 = sbbprj.get_shapefiles()

    assert not df1.empty
    assert isinstance(df2, pd.DataFrame)


def test_get_tv2folders(root=root):

    sbbprj = SbbProjects(root)

    df = sbbprj.get_tv2folders(relpaths=True, include='selected')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    df = sbbprj.get_tv2folders(relpaths=True, include='ambiguous')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    df = sbbprj.get_tv2folders(relpaths=True, include='duplicates')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    df = sbbprj.get_tv2folders(relpaths=True, include='all')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    #assert isinstance(sr, Series)
    #assert not sr.empty


def test_split_projectnames(root=root):

    sbbprj = SbbProjects(root)
    df = sbbprj.split_projectnames()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


