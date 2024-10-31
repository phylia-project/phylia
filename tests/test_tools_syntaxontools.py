
import pytest
from pandas import Series

from phylia.tools._syntaxontools import get_class
from phylia.tools._syntaxontools import get_synlevel
from phylia.tools._syntaxontools import get_possible_levels
import phylia

@pytest.fixture
def sbbsyn():
    syn = phylia.data.sbbcat_syntaxa()
    #syn.index.name = 'syntaxoncode'
    return syn

@pytest.fixture
def rvvnsyn():
    syn = phylia.data.rvvn_syntaxa()
    return syn

# test sbbcat
# -----------

def test_get_synlevel(sbbsyn):
    syn = Series(sbbsyn.index)
    sr = syn.apply(get_synlevel)
    assert isinstance(sr, Series)
    assert not sr.empty

def test_get_class(sbbsyn):
    syn = Series(sbbsyn.index)
    sr = syn.apply(get_class)
    assert isinstance(sr,Series)
    assert not sr.empty
    
def test_sbb_syntaxon_levels(sbbsyn):
    synlevels = get_possible_levels(system='sbbcat')
    assert isinstance(synlevels, list)

    theoretical = ['09','09-a','09/b','09A','09A-a','09A/a','09A1','09A2a','400']
    results = []
    for item in theoretical:
        res = get_synlevel(item, system='sbbcat')
        assert res is not None
        results.append(res)
    assert sorted(results) == sorted(synlevels)

def test_rvvn_syntaxon_levels(rvvnsyn):

    synlevels = get_possible_levels(system='rvvn')
    assert isinstance(synlevels, list)

    theoretical = ['09', '09A', '09AA', '09AA01','09AA02A', '9RG01', '9DG01']
    results = []
    for item in theoretical:
        res = get_synlevel(item, system='rvvn')
        assert res is not None
        results.append(res)
    assert len(results) == len(synlevels)
    #TODO: assert sorted(results) == sorted(synlevels)

    theoretical = ['9', '9A', '9Aa', '9Aa01','9Aa02a', '9RG01', '9DG01']
    results = []
    for item in theoretical:
        res = get_synlevel(item, system='rvvn')
        assert res is not None
        results.append(res)
    assert len(results) == len(synlevels)
    #TODO: assert sorted(results) == sorted(synlevels)
