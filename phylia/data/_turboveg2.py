"""Tables with definitions of Turboveg2 database files."""

import pandas as _pd
from importlib import resources as _resources
from . import _turboveg2_data

def tvabund_definition():
    """Table definition of Turboveg2 tvabdund.dbf file."""
    srcfile = (_resources.files(_turboveg2_data) / 'definition_tvabund.csv')
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
    srcfile = (_resources.files(_turboveg2_data) / 'definition_tvhabita.csv')
    data = _pd.read_csv(srcfile, encoding='latin-1')
    data.columns = data.columns.str.lower()
    return data.set_index('fieldnumber')


def tvremarks_definition():
    """Table definition of Turboveg2 remarks.dbf file."""
    srcfile = (_resources.files(_turboveg2_data) / 'definition_remarks.csv')
    data = _pd.read_csv(srcfile, encoding='latin-1')
    data.columns = data.columns.str.lower()
    return data.set_index('fieldnumber')

