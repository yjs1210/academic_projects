# Your implementation goes in this file.
from src.BaseDataTable import BaseDataTable
import csv
import copy
import json


class Index():
    def __init__(self):
        self._placeholder = None

    def to_json(self):
        result = {}
        result["name"] = self.name
        result["columns"] = self.columns
        result["kind"]  = self.kind
        result["table_name"]  = self.table_name
        result["index_data"] = self._index_data
        return result


    
class CSVDataTable(BaseDataTable):
    
    def debug_message(self, *m):
        """
        Prints some debug information if self._debug is True
        :param m: List of things to print.
        :return: None
        """
        if self._debug:
            print(" *** DEBUG:", *m)
            

    def __init__(self, table_name, connect_info, key_columns=None, debug=True):
        """

        :param table_name: Name of the table. This is the table name for an RDB table or the file name for
            a CSV file holding data.
        :param connect_info: Dictionary of parameters necessary to connect to the data. See examples in subclasses.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
            A primary key is a set of columns whose values are unique and uniquely identify a row. For Appearances,
            the columns are ['playerID', 'teamID', 'yearID']
        :param debug: If true, print debug messages.
        """

        super().__init__(table_name, connect_info, key_columns, debug)
        self._rows = None
        self._column_names = None
        self.debug = debug
            
    def __str__(self):
        result = str(type(self)) + ": name = " + self.table_name
        result += "\nconnect_info = " +str(self.connect_info)
        result += '\nkey columns = : ' + str(self._key_columns) + '\n'
        
        if self._column_names is not None:
            result += "\nColumn names = " +str(self._column_names)
        if self._rows is not None:
            result += '\nrow numbers: ' + str(len(self._rows))
        
        
        return result
    
    def _get_keys(self,row):
        out = [row[k] for k in self._key_columns]
        if len(out) != len(self._key_columns):
            raise ValueError("Wrong Length or duplicate keys")
        return out 
    
    def _add_row(self, row):
        if self._rows is None:
            self._rows = []
        
        keys = self._get_keys(row)
        check = self.find_by_primary_key(keys)
        
        if check is not None:
            raise ValueError("Duplicated keys detected")
            
        for k, v in row.items():
            if k not in self._column_names:
                raise ValueError(k+" not in columns")

        self._rows.append(row)
    
    def load(self):
        directory= self._connect_info['directory'] + self._connect_info['file_name']
        self._rows = []
        with open(directory, mode='r') as input_rows:
            csv_reader = csv.DictReader(input_rows)
            for row in csv_reader:
                if self._column_names is None:
                    self._column_names = list(row.keys())
                if self._rows is None:
                    self._rows = []
                self._add_row(row)
    
    def save(self):

        d = {
            "state":{
                "table_name" : self._table_name,
                "primary_key_columns":self._key_columns,
                "next_rid": self._get_next_row_id(),
                "column_names": self._column_names
            }
        }

        fn = CSVDataTable._default_directory + self._table_name + ".json"
        d["rows"] = self._rows

        for k,v in self._indexes.items():
            idxs = d.get("indexes", {})
            idx_string = v.to_json()
            idxs[k] = idx_string
            d['indexes'] = idxs
        
        d = json.dumps(d, indent=2)
        with open(fn,"w+") as outfile:
            outfile.write(d)

    @TODO    
    def _get_next_row_id(self):
        return 1
    
    def _check_keys(self, key_fields): 
        if len(self._key_columns) != len(key_fields):
            raise ValueError("Entered wrong key_fields please try entering " + ",".join(self._key_columns))
                
    def _check_fields(self, fields):
        actual_fields = self._column_names
        for i in fields:
            if (i not in actual_fields):
                raise ValueError("Field "+ i+ " does not exist")
    
    def _project(self, row, field_list):
        if field_list is None:
            return row
        else:
            return {f:row[f] for f in field_list}

    def find_by_primary_key(self, key_fields, field_list=None):
        """

        :param key_fields: The values for the key_columns, in order, to use to find a record. For example,
            for Appearances this could be ['willite01', 'BOS', '1960']
        :param field_list: A subset of the fields of the record to return. The CSV file or RDB table may have many
            additional columns, but the caller only requests this subset.
        :return: None, or a dictionary containing the columns/values for the row.
        """
        try:
            self._check_keys(key_fields)
            template = dict(zip(self._key_columns, key_fields))
            result = self.find_by_template(template, field_list)
            if not result is None:
                return result
            else:
                return None
    
        except Exception as e:
            print("Got exception = ", e)
            raise e


    def _matches_template(self, tmp, row):
        """

        :param template: A dictionary of the form
            { "field1" : value1,
            "field2": value2, ...}.
            The function will return
            a derived table containing the rows that match the template.

            :param row: An ordered dict
        """
        if tmp is None:
            return True
        
        for key in tmp.keys():
            value = row.get(key,None)
            if tmp[key] != value:
                return False

        return True

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None):
        """

        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}. The function will return
            a derived table containing the rows that match the template.
        :param field_list: A list of requested fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A derived table containing the computed rows.
        """
        
        
        from DerivedDataTable import DerivedDataTable
        if field_list is not None:
            self._check_fields(field_list)

        out = None
        for r in self._rows:
            if self._matches_template(template, r):
                if out is None:
                    out = []
                new_r = self._project(r, field_list)
                out.append(copy.copy(new_r))
                
        if out is not None:
            out = DerivedDataTable("FBT:" + self._table_name, out)
        return out

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records. Raises an exception if this
            creates a duplicate primary key.
        :return: None
        """
        self._add_row(new_record)

    def delete_by_template(self, template):
        """

        Deletes all records that match the template.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        cnt = 0
        new_rows = []
        for r in self._rows:
            if not self._matches_template(template, r):
                new_rows.append(copy.copy(r))
            else:
                cnt +=1
        self._rows = new_rows
        return cnt

    def delete_by_key(self, key_fields):
        """

        Delete record with corresponding key.

        :param key_fields: List containing the values for the key columns
        :return: A count of the rows deleted.
        """

        self._check_keys(key_fields)
        template = dict(zip(self._key_columns, key_fields))
        return self.delete_by_template(template)
    

    def update_by_template(self, template, new_values):
        """

        :param template: A template that defines which matching rows to update.
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """

        self._check_fields(new_values.keys())

        key_check = []
        for k in new_values:
            if k in self._key_columns:
                key_check.append(k)
        
        if key_check != []:
            key_row_check = []
            
            for row in self._rows:
                key_row = dict()
                for key in self._key_columns:
                    key_row_check[key] = row[key]
                if self._matches_template(template, row):
                    for key in key_check:
                        key_row[key] = new_values[key]
                        
                key_row_check.append(copy.copy(key_row))
                
            for i in range(len(key_row_check)-1):
                for j in range(i + 1, len(key_row_check)):
                    if key_row_check[i] == key_row_check[j]:
                        raise ValueError("Update will create duplicate primary key")
                        
        out = 0
        for row in self._rows:
            if self._matches_template(template, row):
                out += 1
                for k, v in new_values.items():
                    row[k] = v
        return out

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of values for primary key fields
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """

        self._check_keys(key_fields)
        template = dict(zip(self._key_columns, key_fields))
        return self.update_by_template(template, new_values)