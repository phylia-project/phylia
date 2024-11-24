
import pytest
from pandas import Series

from phylia.tools import syntaxontools
import phylia

@pytest.fixture
def sbbsyn():
    syn = phylia.data.sbbcat_syntaxa()
    return syn

@pytest.fixture
def rvvnsyn():
    syn = phylia.data.synbiosys.rvvn_syntaxa()
    return syn

# test sbbcat
# -----------

def test_get_synlevel(sbbsyn):
    syn = Series(sbbsyn.index)
    sr = syn.apply(syntaxontools.syntaxonlevel)
    assert isinstance(sr, Series)
    assert not sr.empty

def test_get_class(sbbsyn):
    syn = Series(sbbsyn.index)
    sr = syn.apply(syntaxontools.syntaxonclass)
    assert isinstance(sr,Series)
    assert not sr.empty

def test_reference_levels():
    synlevels = syntaxontools.reference_levels(reference='sbbcat')
    assert isinstance(synlevels, list)

    synlevels = syntaxontools.reference_levels(reference='vvn')
    assert isinstance(synlevels, list)
    
def test_sbb_syntaxon_level(sbbsyn):
    theoretical = ['09','09-a','09/b','09A','09A-a','09A/a','09A1','09A2a','400']
    results = []
    for item in theoretical:
        res = syntaxontools.syntaxonlevel(item, reference='sbbcat')
        assert res is not None
        results.append(res)

    synlevels = syntaxontools.reference_levels(reference='sbbcat')
    assert sorted(results) == sorted(synlevels)


def test_rvvn_syntaxon_level(rvvnsyn):
    theoretical = ['r09', 'r09A', 'r09AA', 'r09AA01','r09AA02A', 'r9RG01', 'r9DG01']
    results = []
    for item in theoretical:
        res = syntaxontools.syntaxonlevel(item, reference='vvn')
        assert res is not None
        results.append(res)

    synlevels = syntaxontools.reference_levels(reference='vvn')
    assert len(results) == len(synlevels)
    #TODO: assert sorted(results) == sorted(synlevels)

    theoretical = ['9', '9A', '9Aa', '9Aa01','9Aa02a', '9RG01', '9DG01']
    results = []
    for item in theoretical:
        res = syntaxontools.syntaxonlevel(item, reference='vvn')
        assert res is not None
        results.append(res)
    assert len(results) == len(synlevels)
    #TODO: assert sorted(results) == sorted(synlevels)
