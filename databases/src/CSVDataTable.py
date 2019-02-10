# Your implementation goes in this file.
from BaseDataTable import BaseDataTable
import csv
import copy

class CSVDataTable(BaseDataTable):

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
        self._num_rows = 0
        self._rows = []
        self._field_names = []

    def __str__(self):
        result = ''
        result += 'Key fields: ' + str(self._key_columns) + '\n'
        result += 'No. of rows: ' + str(self._num_rows)
        return result

    def _validate_key_field(self, key_fields):
        if len(key_fields) != len(self._key_columns):
            raise Exception("Wrong Length of Keys")

    def _validate_field_list(self, field_list):
        if field_list is not None:
            for field in field_list:
                if field not in self._field_names:
                    raise Exception("'{}' is not a valid column name".format(field))

    def _validate_new_key(self, key_fields, already_dict=False):
        if len(key_fields) != len(self._key_columns):
            raise Exception("Wrong Length Keys")
        template = key_fields
        if not already_dict:
            template = dict(zip(self._key_columns, key_fields))
        for r in self._rows:
            if self._matches_template(template, r):
                raise Exception("Duplicate Primary Key")

    def _validate_new_record(self, new_record):
        keys = {}
        for k, v in new_record.items():
            if k not in self._field_names:
                raise Exception("{} is not a valid column name")
            if k in self._key_columns:
                keys[k] = v
        self._validate_new_key(keys, True)

    def find_by_primary_key(self, key_fields, field_list=None):
        """

        :param key_fields: The values for the key_columns, in order, to use to find a record. For example,
            for Appearances this could be ['willite01', 'BOS', '1960']
        :param field_list: A subset of the fields of the record to return. The CSV file or RDB table may have many
            additional columns, but the caller only requests this subset.
        :return: None, or a dictionary containing the columns/values for the row.
        """

        self._validate_key_field(key_fields)

        template = dict(zip(self._key_columns, key_fields))

        result = self.find_by_template(template, field_list)

        if result is not None:
            result = result._rows[0]

        return result

    # TODO: write dis
    def load(self):
        path = self._connect_info['directory'] + self._connect_info['file_name']
        self._rows = []
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            self._field_names = csv_reader.fieldnames
            line_count = 0
            for row in csv_reader:
                self._rows.append(row)
                line_count += 1
            self._num_rows = line_count

    def _project(self, row, field_list):
        if field_list is None:
            return row
        else:
            return {f:row[f] for f in field_list}

    # TODO: write dis too
    def _matches_template(self, template, row):
        """

        :param template: A dictionary of the form
            { "field1" : value1,
            "field2": value2, ...}.
            The function will return
            a derived table containing the rows that match the template.

            :param row: An ordered dict
        """

        for key, value in template.items():
            if not (key in row and value == row[key]):
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

        self._validate_field_list(field_list)

        from DerivedDataTable import DerivedDataTable

        result = None

        for r in self._rows:

            if self._matches_template(template, r):

                if result is None:
                    result = []

                new_r = self._project(r, field_list)

                result.append(new_r)

        if result is not None:
            result = DerivedDataTable("FBT:" + self._table_name, result)

        return result

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records. Raises an exception if this
            creates a duplicate primary key.
        :return: None
        """
        self._validate_new_record(new_record)

        for name in self._field_names:
            if name not in new_record:
                new_record[name] = 'NA'

        self._rows.append(new_record)

    def delete_by_template(self, template):
        """

        Deletes all records that match the template.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        count = 0

        i = 0
        while i < len(self._rows):
            row = self._rows[i]
            if self._matches_template(template, row):
                count += 1
                self._rows.pop(i)
                i -= 1
            i += 1
        return count

    def delete_by_key(self, key_fields):
        """

        Delete record with corresponding key.

        :param key_fields: List containing the values for the key columns
        :return: A count of the rows deleted.
        """

        self._validate_key_field(key_fields)

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

        self._validate_field_list(new_values.keys())

        keys = []
        for k in new_values:
            if k in self._key_columns:
                keys.append(k)

        if len(keys) > 0:
            key_rows = []
            for row in self._rows:
                key_row = {}
                for key in self._key_columns:
                    key_row[key] = row[key]
                if self._matches_template(template, row):
                    for key in keys:
                        key_row[key] = new_values[key]
                key_rows.append(key_row)
            for i in range(len(key_rows)-1):
                for j in range(i + 1, len(key_rows)):
                    if key_rows[i] == key_rows[j]:
                        raise Exception("Update will create duplicate primary key")

        count = 0
        for row in self._rows:
            if self._matches_template(template, row):
                count += 1
                for k, v in new_values.items():
                    row[k] = v

        return count

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of values for primary key fields
        :param new_values: A dictionary containing fields and the values to set for the corresponding fields
            in the records. This returns an error if the update would create a duplicate primary key. NO ROWS are
            update on this error.
        :return: The number of rows updates.
        """

        self._validate_key_field(key_fields)

        template = dict(zip(self._key_columns, key_fields))

        return self.update_by_template(template, new_values)