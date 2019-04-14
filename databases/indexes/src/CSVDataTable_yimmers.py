import json
import copy


class Index():

    def __init__(self, index_name, index_columns,  kind):
        self._index_name = index_name
        self._columns = index_columns
        self._kind = kind
        self._index_data = None

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
            bucket.append(rid)
        bucket.append(rid)
        self._index_data[key] = bucket

    def to_json(self):

        # Converts the index data and state to a JSON object
        # returns a JSON representation

        result = {}
        result['name'] = self.name
        result['columns'] = self.columns
        result['kind'] = self.kind
        result['table_name'] = self.table_name
        result['index_data'] = self._index_data
        return result


class CSVDataTable():

    def __init__(self, table_name, column_names=None, primary_key_columns=None, loadit=False):
        # param table_name: logicalname of the table, also name of the fileinDB directory
        # param_column_names: name of allowed columns in the data table
        # param key_columsn: list in order ofthe columns (fields) that comprise the primary key
        # praram loadit: if this is true,the load method will set the values

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

        self._indexes[index_name] = Index(index_name=index_name, index_columns=column_list, kind=kind)
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
                'next_rid': self._get_next_row_id(),
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
            self.primary_key_columns = state['primary_key_columns']
            self._next_row_id = state['next_rid']
            self._column_names = state['column_names']
            self._rows = d['rows']

            for k, v in d['indexes'].items():
                idx = Index(loadit=v, table=self)
                if self._indexes is None:
                    self._indexes = {}
                self._indexes[k] = idx

            for k, v in d['indexes'].items():
                idx = Index


    def load_from_rows(self, table_name, rows):
        #@TODO: implement dis
        pass

    def get_rows(self):
        #@TODO: implement dis
        pass

    def get_best_index(self):
        #@TODO: implement dis
        pass

    def find_by_template(self, tmp, fields=None, use_index=True):

        """"""
        # tmp - template tomatch
        # fields - fields to get, ie project clause
        # use_index = if true, we can use index if false cannot

        # """"""


        ## New code from OH 4/08
        if tmp is None:
            new_t = CSVDataTable(table_name="Derived:" + self._table_name, loadit=True)
            new_t.load_from_rows(table_name="Derived:" + self._table_name, rows=self.get_rows())

        idx = self.get_best_index(tmp)
        #logging.debug("Using index = %s", idx)

        if idx is None or use_index==False:
            result = self.find_by_scan_template(tmp, self.get_rows())
        else:
            idx = self._indexes[idx]
            res = reslf.find_by_index(tmp, idx)
            result = self.find_by_scan_template(tmp, res)

        if result:
            final_r = []
            for r in result:
                final_new_r = {k:r[k] for k in fields}
                final_r.append(final_new_r)

        new_t = CSVDataTable(table_name="Derived:" + self._table_name, loadit=True)
        new_t.load_from_rows(table_name="Derived:" + self._table_name, rows=final_r)

        return new_t

        '''
        idx = self.get_best_index(tmp)
        logging.debug('Using index = %s', idx)

        if idx is None or use_index == False:
            result = self.find_by_scan_template(tmp, self.get_rows())
        else:
            idx = self._indexes[idx]
            res = self.find_by_index(tmp, idx)
            result = self.find_by_scan_template(tmp, res)
        new_t = CSVDataTable(table_name='Derived:' + self._table_name, loadit=True)
        new_t.load_from_rows(table_name='Derived:' + self._table_name, rows=result)

        return new_t
        '''




    def __choose_scan_probe_table__(self, right_r, on_fields):
        left_path, left_count = self.__get_access_path__(on_fields)
        right_path, right_count = right_r.__get_access_path__(on_fields)

        if left_path is None and right_path is None:
            return self, right_r
        elif left_path is None and right_path is not None:
            return self, right_r
        elif left_path is not None and right_path is None:
            return right_r, self
        elif right_count < left_count:
            return self, right_r
        else:
            return right_r, self


    # TINKER WITH CODE TO MAKE IT WORK
    def join(self, right_r, on_fields, where_template=None):
        scan_t, probe_t = self.__choose_scan_probe_table__(right_r, on_fields)

        scan_sub_template = scan_t.__get_sub_where_template(where_template)
        probe_sub_template = probe_t.__get_sub_where_template(where_template)

        scan_rows = self.find_by_template(scan_sub_template)

        join_result = []

        for l_r in scan_rows:
            on_template = self.__get_on_template__(l_r, on_fields)
            if probe_sub_template is not None:
                right_where = {**on_temaplte, **probe_sub_template}
            else:
                right_where = on_template
            current_right_rows = right_r.find_by_template(right_where)
            if current_right_rows is not None and len(current_right_rows) > 0:
                new_rows = self.__join_rows__([l_r], current_right_rows, on_fields)
                join_result.extend(new_rows)

        join_result = self.__table_from_rows__(
            "JOIN(" + self.__table_name__ + "," + right_r.__table_name__ + ")",
            None,
            join_result
        )

        return join_result