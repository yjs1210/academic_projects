import json
import pandas
import copy
import csv
import logging

class Index():

    def __init__(self, index_name, table, index_columns,  kind, index_data=None):
        self._index_name = index_name
        self._columns = index_columns
        self._kind = kind
        self._index_data = index_data
        self._table = table

    def to_json(self):

        # Converts the index data and state to a JSON object
        # returns a JSON representation

        result = {}
        result['name'] = self._index_name
        result['columns'] = self._columns
        result['kind'] = self._kind
        result['table_name'] = self._table._table_name
        result['index_data'] = self._index_data
        return result

    def compute_key(self, row):
        key_v = [row[k] for k in self._columns]
        key_v = "_".join(key_v)
        return key_v

    def add_to_index(self, row, rid):
        if self._index_data is None:
            self._index_data = {}

        key = self.compute_key(row)
        bucket = self._index_data.get(key, [])
        if self._kind != "INDEX":
            if len(bucket) > 0:
                raise KeyError("Duplicate key")

        #bucket will look like [rid], but maybe we want it like: {rid: {data}}
        bucket.append(rid)
        self._index_data[key] = bucket


class CSVDataTable():
    _default_directory = '/Users/yimin/Desktop/Columbia/Spring 2019/Databases/HW3/'

    def __init__(self, table_name, column_names=None, primary_key_columns=None, loadit=False):
        # param table_name: logical name of the table, also name of the fileinDB directory
        # param_column_names: name of allowed columns in the data table
        # param key_colums n: list in order of the columns (fields) that comprise the primary key
        # param loadit: if this is true, the load method will set the values

        self._table_name = table_name
        self._primary_key_columns = primary_key_columns
        self._column_names = column_names

        # dictionary containing index datastructures
        self._indexes = None

        if not loadit:
            # some parameters are mandatory if this is not a load.
            if column_names is None or table_name is None:
                raise ValueError('Did not provide table_name or columns_names for creating table')
            self._next_row_id = 1

            # dictionarythat will hold the rows:
            self._rows = {}

            if primary_key_columns:
                self.add_index('PRIMARY', self._primary_key_columns, 'PRIMARY')
        else:
            self.load()

    def get_next_row_id(self):
        self._next_row_id += 1
        return self._next_row_id

    def insert(self, r):

        if self._rows is None:
            self._rows = {}

        rid = self.get_next_row_id()

        if self._indexes is not None:
            for k,v in self._indexes.items():
                v.add_to_index(r, rid)

        self._rows[rid] = copy.copy(r)

    def import_data(self, rows):
        for r in rows:
            self.insert(r)

    def add_index(self, index_name, column_list, kind):
        if self._indexes is None:
            self._indexes = {}

        self._indexes[index_name] = Index(table=self, index_name=index_name, index_columns=column_list, kind=kind)
        self.build(index_name)

    def build(self, i_name):
        idx = self._indexes[i_name]
        for k, v in self._rows.items():  # k is the row id, and v is the row
            idx.add_to_index(v, k)

    def save(self):
        d = {
            "state": {  # state element in this dict are these attributes of the datatable
                'table_name': self._table_name,
                'primary_key_columns': self._primary_key_columns,
                'next_rid': self._next_row_id,
                'column_names': self._column_names
            }
        }

        fn = CSVDataTable._default_directory + self._table_name + ".json"
        d['rows'] = self._rows

        for k, v in self._indexes.items():
            idxs = d.get('indexes', {})
            idx_string = v.to_json()
            idxs[k] = idx_string
            d['indexes'] = idxs

        d = json.dumps(d, indent=2)
        with open(fn, 'w+') as outfile:
            outfile.write(d)

    def load(self):

        fn = CSVDataTable._default_directory + self._table_name + ".json"
        with open(fn, 'r') as infile:
            d = json.load(infile)

            state = d['state']
            self._table_name = state['table_name']
            self._columns = state['primary_key_columns']
            self._next_row_id = state['next_rid']
            self._column_names = state['column_names']
            self._rows = d['rows']

            for k, v in d['indexes'].items():
                #idx = Index(loadit=v, table=self)
                idx = Index(index_name=v['name'], table=self, index_columns=v['columns'], kind=v['kind'], index_data=v['index_data'])
                idx
                if self._indexes is None:
                    self._indexes = {}
                self._indexes[k] = idx