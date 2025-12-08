"""Tables with definitions of Turboveg2 database files."""

import pandas as _pd
from importlib import resources as _resources
#import importlib as _importlib
import geopandas as _gpd
from . import _data_turboveg2

def tvabund_definition():
    """Table definition of Turboveg2 tvabdund.dbf file."""
    srcfile = (_resources.files(_data_turboveg2) / 'definition_tvabund.csv')
    data = _pd.read_csv(srcfile, encoding='latin-1')
    data.columns = data.columns.str.lower()
    return data.set_index('fieldnumber')


def tvabund_fieldtypes():
    data = tvabund_definition()
    typedict = dict(zip(
        data['fieldname'].values,
        data['type'].values,
        ))
    return typedict


def tvhabita_definition():
    """Table definition of Turboveg2 tvhabita.dbf file."""
    srcfile = (_resources.files(_data_turboveg2) / 'definition_tvhabita.csv')
    data = _pd.read_csv(srcfile, encoding='latin-1')
    data.columns = data.columns.str.lower()
    return data.set_index('fieldnumber')


def tvremarks_definition():
    """Table definition of Turboveg2 remarks.dbf file."""
    srcfile = (_resources.files(_data_turboveg2) / 'definition_remarks.csv')
    data = _pd.read_csv(srcfile, encoding='latin-1')
    data.columns = data.columns.str.lower()
    return data.set_index('fieldnumber')


def floralist_nederlnd():
    """Turboveg2 taxonlist Floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Nederlnd') / 'species.dbf'
    data = _gpd.read_file(srcfile)
    return data


def floralist_floranld():
    """Turboveg2 taxonlist Floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld') / 'species.dbf'
    data = _gpd.read_file(srcfile)
    return data


def floralist_floranld_2013():
    """Turboveg2 taxonlist Floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld_2013') / 'species.dbf'
    data = _gpd.read_file(srcfile)
    return data


def floralist_floranld_2017():
    """Turboveg2 taxonlist Floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld_2017') / 'species.dbf'
    data = _gpd.read_file(srcfile)
    return data


def floralist_floranld_2020():
    """Turboveg2 taxonlist Floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld_2020') / 'species.dbf'
    data = _gpd.read_file(srcfile)
    return data


def ecodata_nederlnd():
    """Turboveg2 ecodatabase for floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Nederlnd') / 'ecodbase.dbf'
    data = _gpd.read_file(srcfile)
    return data.set_index('SPECIES_NR', verify_integrity=True)


def ecodata_floranld():
    """Turboveg2 ecodatabase for floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld') / 'ecodbase.dbf'
    data = _gpd.read_file(srcfile)
    return data.set_index('SPECIES_NR', verify_integrity=True)


def ecodata_floranld_2013():
    """Turboveg2 ecodatabase for floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld_2013') / 'ecodbase.dbf'
    data = _gpd.read_file(srcfile)
    return data.set_index('SPECIES_NR', verify_integrity=True)


def ecodata_floranld_2017():
    """Turboveg2 ecodatabase for floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld_2017') / 'ecodbase.dbf'
    data = _gpd.read_file(srcfile)
    return data.set_index('SPECIES_NR', verify_integrity=True)


def ecodata_floranld_2020():
    """Turboveg2 ecodatabase for floranld."""
    srcfile = _resources.files(_data_turboveg2).joinpath('Floranld_2020') / 'ecodbase.dbf'
    data = _gpd.read_file(srcfile)
    return data.set_index('SPECIES_NR', verify_integrity=True)


