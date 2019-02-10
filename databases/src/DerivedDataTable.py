# Your implementation goes in this file.
from BaseDataTable import BaseDataTable

class DerivedDataTable(BaseDataTable):
                
    def __init__(self, table_name, rows):
        """

        :param table_name: The name of the RDB table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        # Initialize and store information in the parent class.
        self._table_name = table_name
        self._rows = rows
        self._key_columns = None
        self._debug = None
 
    def find_by_primary_key(self, key_fields, field_list=None):
        """

        :param key_fields: The values for the key_columns, in order, to use to find a record. For example,
            for Appearances this could be ['willite01', 'BOS', '1960']
        :param field_list: A subset of the fields of the record to return. The CSV file or RDB table may have many
            additional columns, but the caller only requests this subset.
        :return: None, or a dictionary containing the columns/values for the row.
        """
        pass

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None, commit=True):
        """

        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
        :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A list containing dictionaries. A dictionary is in the list representing each record
            that matches the template. The dictionary only contains the requested fields.
        """
        try:
            t_name = self._table_name   
            data = self._rows
            
            if data is None:
                return None
            
            if(len(data)==0):
                return None
            
            if(not all(key in data[0].keys() for key in template.keys())):
                raise KeyError('Specified columns in field_list are not found in the original data')
                
            out_data = []
            for row in iter(data):
                for key,val in template.items():
                    if(row[key] != val):
                        continue
                    if field_list is None:
                        out_data.append(row)
                    else:
                        row_out = dict((k, row[k]) for k in field_list.keys())
                        out_data.append(row_out)
            if len(row_out) ==0:
                return None
            
            return DerivedDataTable(t_name,out_data)
        
        except Exception as e:
            print("Got exception = ", e)
            raise e  
                

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records. Raises an exception if this
            creates a duplicate primary key.
        :return: None
        """
        pass

    def delete_by_template(self, template):
        """

        Deletes all records that match the template.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        pass

    def delete_by_key(self, key_fields):
        """

        Delete record with corresponding key.

        :param key_fields: List containing the values for the key columns
        :return: A count of the rows deleted.
        """
        pass

    def update_by_template(self, template, new_values):
        """

        :param template: A template that defines which matching rows to update.
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """
        pass

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of values for primary key fields
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """
        pass
