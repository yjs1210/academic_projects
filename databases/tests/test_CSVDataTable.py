from CSVDataTable import CSVDataTable

connect_info = {
    'directory': '../data/',
    'file_name': 'demographics_by_zip.csv'
}

offices = CSVDataTable('Offices', key_columns=['zipcode'], connect_info=connect_info)
#%%
print(offices)

offices.load()
#%%
print(offices)

print(offices._rows[0])

print('field names: ', offices._field_names)

template = {
    'zipcode': '10004'
}

template1 = {
    'zipcode': '10004'
}

#field_list = ['officeCode', 'city']

#bool = offices._matches_template(template, offices._rows[0])

#print(bool)

res = offices.find_by_template(template1)._rows
#%%
print(res, '\n')

res = offices.find_by_primary_key(['1'])

print(res, '\n')

key_field = ['12']

offices._validate_new_key(key_field)

print('New key: {} is valid'.format(key_field), '\n')

newOffice = {
    'officeCode': '12'
}

offices.insert(newOffice)

res = offices.find_by_primary_key(['12'])

print('after insert: ', res, '\n')

new_values = {
    "city": "DankTon"
}

offices.update_by_template(template1, new_values)

print('Offices are: ', offices._rows)

