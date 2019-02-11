from DerivedDataTable import DerivedDataTable
from CSVDataTable import CSVDataTable
import pytest


def get_offices():
    connect_info = {
        'directory': '/Users/yimin/Desktop/Columbia/Spring 2019/Databases/w4111-Databases/HW_Assignments/HW1/Data/',
        'file_name': 'offices.csv'
    }
    offices = CSVDataTable('offices', key_columns=['officeCode'], connect_info=connect_info)
    offices.load()
    DDT = offices.find_by_template({})
    return DDT


def test_find_by_template():
    offices = get_offices()
    template = {'country': 'USA'}
    result = offices.find_by_template(template)
    assert isinstance(result, DerivedDataTable)
    assert len(result._rows) == 6
    for row in result._rows:
        assert row['country'] == 'USA'

    empty = {}
    result = offices.find_by_template(empty)
    assert len(result._rows) == 10

    wrong = {'color': 'blue'}
    result = offices.find_by_template(wrong)
    assert result is None


def test_find_by_template_with_fields():
    offices = get_offices()
    template = {'country': 'USA'}
    fields = ['officeCode', 'city']
    result = offices.find_by_template(template, field_list=fields)
    for row in result._rows:
        assert 'officeCode' in row
        assert 'city' in row
        assert 'country' not in row

    wrong_field = ['ccity']
    with pytest.raises(Exception):
        result = offices.find_by_template(template, field_list=wrong_field)



test_find_by_template()
test_find_by_template_with_fields()