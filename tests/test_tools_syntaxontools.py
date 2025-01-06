
import pytest
from pandas import Series
import pandas as pd
import numpy as np

from phylia.tools import syntaxontools
import phylia

@pytest.fixture
def sbbsyn():
    syn = phylia.data.cmsi.vegetationtypes(typology='sbbcat', 
        current_only=False, verbose=False)
    return syn

@pytest.fixture
def rvvnsyn():
    syn = phylia.data.synbiosys.rvvn_syntaxa()
    return syn


def test_for_unexpected_change_in_constants():

    assert len(syntaxontools.SUPPORTED_REFERENCE_SYSTEMS)==3
    assert len(syntaxontools.SYNTAXON_ORDER)==11


def test_reference_levels():

    reflev = syntaxontools.reference_levels('sbbcat')
    assert isinstance(reflev, list)
    assert len(reflev)==9

    reflev = syntaxontools.reference_levels('rvvn')
    assert isinstance(reflev, list)
    assert len(reflev)==9

    reflev = syntaxontools.reference_levels('vvn')
    assert isinstance(reflev, list)
    assert len(reflev)==9


def test_reference_patterns():

    refpat = syntaxontools.reference_patterns(reference='sbbcat')
    assert isinstance(refpat, dict)
    assert len(refpat)==9

    refpat = syntaxontools.reference_patterns(reference='rvvn')
    assert isinstance(refpat, dict)
    assert len(refpat)==8

    refpat = syntaxontools.reference_patterns(reference='vvn')
    assert isinstance(refpat, dict)
    assert len(refpat)==8


def test_validate_string():
    # validate_string is a helper function for syntaxon_validate

    testcodes = [str(x) for x in syntaxontools.SBB_TESTCODES]
    validated = [syntaxontools._syntaxon_validate_string(x) 
        for x in testcodes]

    assert all(isinstance(x, str) for x in validated if x is not None)

    testcodes = [str(x) for x in syntaxontools.VVN_TESTCODES]
    validated = [syntaxontools._syntaxon_validate_string(x) 
        for x in testcodes]

    assert all(isinstance(x, str) for x in validated if x is not None)


def test_syntaxon_validate():

    # input pandas series
    validated = syntaxontools.syntaxon_validate(Series(syntaxontools.SBB_TESTCODES))
    assert isinstance(validated, Series)
    assert not validated.empty

    # input list
    validated = syntaxontools.syntaxon_validate(syntaxontools.SBB_TESTCODES)
    assert isinstance(validated, list)
    assert all(isinstance(x, str) for x in validated if x is not None)

    # input integer (valid code)
    code = 400
    validated = syntaxontools.syntaxon_validate(code)
    assert isinstance(validated, str)

    # input string
    code = '400'
    validated = syntaxontools.syntaxon_validate(code)
    assert isinstance(validated, str)


def test_syntaxonclass_string(sbbsyn):


    testcodes = syntaxontools.SBB_TESTCODES
    synclass = syntaxontools.syntaxonclass(testcodes)
    res = [isinstance(x, str) for x in synclass if not pd.isnull(x)]

    testcodes = syntaxontools.VVN_TESTCODES
    synclass = syntaxontools.syntaxonclass(testcodes)
    res = [isinstance(x, str) for x in synclass if not pd.isnull(x)]


def test_syntaxonclass():

    # input pandas series
    synclass = syntaxontools.syntaxonclass(Series(syntaxontools.SBB_TESTCODES))
    assert isinstance(synclass, Series)
    assert not synclass.empty

    # input list
    synclass = syntaxontools.syntaxonclass(syntaxontools.SBB_TESTCODES)
    assert isinstance(synclass, list)
    assert all(isinstance(x, str) for x in synclass if not pd.isnull(x))


def test_get_synlevel(sbbsyn):

    syn = Series(sbbsyn.index)
    sr = syn.apply(syntaxontools.syntaxonlevel)
    assert isinstance(sr, Series)
    assert not sr.empty



def test_reference_levels():
    synlevels = syntaxontools.reference_levels(reference='sbbcat')
    assert isinstance(synlevels, list)

    synlevels = syntaxontools.reference_levels(reference='vvn')
    assert isinstance(synlevels, list)


def test_syntaxon_level_with_sbbcat(sbbsyn):

    reference_levels = [x for x in syntaxontools.reference_levels(
        reference='sbbcat') if x!='nvt']    

    valid_codes = ['09','09-a','09/b','09A','09A-a','09A/a','09A1','09A2a',]
    synlevels = []
    for code in valid_codes:
        res = syntaxontools.syntaxonlevel(code, reference='sbbcat')
        assert res is not None
        if not code=='nvt':
            synlevels.append(res)

    assert sorted(synlevels) == sorted(reference_levels)


def test_syntaxon_level_with_rvvn(rvvnsyn):

    reference_levels = [x for x in syntaxontools.reference_levels(
        reference='vvn') if x!='nvt']

    # test new style Revisie codes
    valid_codes = ['r09', 'r09A', 'r09AA', 'r09AA01','r09AA02A', 
        'r9RG01', 'r9DG01']
    synlevels = []
    for code in valid_codes:
        res = syntaxontools.syntaxonlevel(code, reference='vvn')
        assert res is not None
        if not code=='nvt':
            synlevels.append(res)

    assert len(synlevels) == len(reference_levels)
    assert sorted(synlevels) == sorted(reference_levels)

    # test old style Vegetatie van Nederland codes
    valid_codes = ['9', '9A', '9Aa', '9Aa01','9Aa02a', '9RG01', '9DG01']
    synlevels = []
    for code in valid_codes:
        res = syntaxontools.syntaxonlevel(code, reference='vvn')
        assert res is not None
        if not code=='nvt':
            synlevels.append(res)

    assert len(synlevels) == len(reference_levels)
    assert sorted(synlevels) == sorted(reference_levels)
