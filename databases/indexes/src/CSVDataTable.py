##James Lee - jl5241
# Your implementation goes in this file.
import csv
import copy
import json


class Index():
    def __init__(self, index_name, table, index_columns,kind, index_data=None):
        self._index_name = index_name
        self._columns = index_columns
        self._kind = kind 
        self._index_data = index_data
        self._table = table

    def compute_key(self,row):
        key_v = [row[k] for k in self._columns]
        key_v = "_".join(key_v)
        return key_v 

    def add_to_index(self,row,rid):
        if self._index_data is None:
            self._index_data = {}
        key = self.compute_key(row)
        bucket = self._index_data.get(key, None)
        if self._kind != "INDEX" and bucket is not None:
                raise KeyError("Duplicate Key")
        else:
            if bucket is None:
                bucket = {}
        bucket[rid] = row
        self._index_data[key] = bucket
   
    def matches_index(self, template):

        k = set(list(template.keys()))
        c = set(self._columns)

        if c.issubset(k):
            if self._index_data is not None:
                kk = len(self._index_data.keys())
            else:
                kk = 0
        else: kk= None 
        
        return kk 

    def to_json(self):
        result = {}
        result["name"] = self._index_name
        result["columns"] = self._columns
        result["kind"]  = self._kind
        result["table_name"]  = self._table._table_name
        result["index_data"] = self._index_data
        return result

    def from_json(self,table,loadit):
        return None
    
    def __str__(self):
        result = str(type(self)) + ": name = " + self._table._table_name
        #result += "\nconnect_info = " +str(self.connect_info)
        result += '\nindex columns = : ' + str(self._columns) + '\n'
        result += '\nindex kind: ' + str(self._kind)

        return result
    
    def find_rows(self,tmp):

        t_keys = tmp.keys()
        t_vals = [tmp[k] for k in self._columns]
        t_s = "_".join(t_vals)

        d = self._index_data.get(t_s,None)

        if d is not None:
            d = list(d.keys())

        return d 

    def get_no_of_entries(self):
        return len(list(self._index_data.keys()))
    
    def delete_from_index(self,row,rid):
        index_key = self.compute_key(row)
        bucket = self._index_data.get(index_key,None)

        if bucket is not None:
            del bucket[rid]

            if len(bucket) == 0:
                del (self._index_data[index_key])

class CSVDataTable():
    _default_directory = 'DB/'
    
    def debug_message(self, *m):
        """
        Prints some debug information if self._debug is True
        :param m: List of things to print.
        :return: None
        """
        if self._debug:
            print(" *** DEBUG:", *m)
            

    def __init__(self, table_name, column_names=None,primary_key_columns=None, debug=True, loadit=False):
        """

        :param table_name: Name of the table. This is the table name for an RDB table or the file name for
            a CSV file holding data.
        :param connect_info: Dictionary of parameters necessary to connect to the data. See examples in subclasses.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
            A primary key is a set of columns whose values are unique and uniquely identify a row. For Appearances,
            the columns are ['playerID', 'teamID', 'yearID']
        :param debug: If true, print debug messages.
        """
        self._primary_key_columns = primary_key_columns
        self._table_name = table_name
        self._column_names = column_names
        self._indexes = None 
        self.debug = debug

        if not loadit:
            if column_names is None or table_name is None:
                raise ValueError("Did not provide table_name for column_names for table create.")
            
            self._next_row_id = 1

            self._rows = {}

            if primary_key_columns:
                self.add_index("PRIMARY",  column_list = self._primary_key_columns, kind ="PRIMARY")
        else: 
            self.load()


            
    def __str__(self):
        result = str(type(self)) + ": name = " + self._table_name
        #result += "\nconnect_info = " +str(self.connect_info)
        result += '\nkey columns = : ' + str(self._primary_key_columns) + '\n'
        
        if self._column_names is not None:
            result += "\nColumn names = " +str(self._column_names)
        if self._rows is not None:
            result += '\nrow numbers: ' + str(len(self._rows))
        if self._indexes is not None:
            result += '\nindexes:' 
            for k,v in self._indexes.items():
                result += '\n index_name :'+ str(v._index_name) + ' index columns: ' +str(v._columns)
        return result

    def add_index(self,name,kind,column_list):

        if kind not in ["PRIMARY","UNIQUE","INDEX"]:
            raise ValueError("Wrong type of index")

        if name is None or column_list is None or kind is None:
            raise ValueError("Could not add index")
        
        if self._indexes is None:
            self._indexes = {}
        
        idx = self._indexes.get(name,None)
        if idx is not None:
            raise ValueError("Dupllicate Index Name")

        self._indexes[name]  = Index(index_name=name,table = self, index_columns = column_list, kind=kind)

        self.build(name)

        #index = Index(index_name=index_name,self, index_columns = columns, kind=kind)
        #self._indexes[index_name]  = index
        #index._build()

    def build(self,i_name):
        idx = self._indexes[i_name]
        for k,v in self._rows.items():
            idx.add_to_index(v,k)       
    
    def import_data(self,rows):
        for r in rows:
            self.insert(r)


    def get_new_row_id(self):
        self._next_row_id +=1
        return self._next_row_id

    def insert(self,r):
        if self._rows is None:
            self._rows = {}
        rid = self.get_new_row_id()

        if self._indexes is not None:
            for k,v in self._indexes.items():
                v.add_to_index(r,rid)

        self._rows[rid]  = copy.copy(r)

    def _get_keys(self,row):
        out = [row[k] for k in self._primary_key_columns]
        if len(out) != len(self._primary_key_columns):
            raise ValueError("Wrong Length or duplicate keys")
        return out 
    

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
                if v['kind'] == 'PRIMARY' and self._primary_key_columns is None: 
                    self._primary_key_columns = v['columns']
        
                if self._indexes is None:
                    self._indexes = {}
                self._indexes[k] = idx

  
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

    def _check_keys(self, key_fields): 
        if len(self._primary_key_columns) != len(key_fields):
            raise ValueError("Entered wrong key_fields please try entering " + ",".join(self._primary_key_columns))
                
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

    def get_rows_with_rids(self):
        return self._rows

    def get_rows(self):
        if self._rows is not None:
            result = []
            for k,v in self._rows.items():
                result.append(v)
        else:
            result = None 
        return result

    def _matches_template(self, row,tmp):
        """

        :param template: A dictionary of the form
            { "field1" : value1,
            "field2": value2, ...}.
            The function will return
            a derived table containing the rows that match the template.

            :param row: An ordered dict
        """
        
        if tmp is None or tmp =={}:
            result = True
        else:

            for key in tmp.keys():
                value = row.get(key,None)
                if tmp[key] != value:
                    return False
        return True

    def get_best_index(self,t):

        best =None
        n = None

        if self._indexes is not None:

            #For every index name and Index Object
            for k,v in self._indexes.items():

                #determine if this index matches the template
                cnt = v.matches_index(t)

                ## If it does
                if cnt is not None:
                    ##if I not have a best. This is best.
                    if best is None:
                        best = cnt   #best value is cnt
                        n =k #name of best index is n
                    else:
                        if cnt>best: #this one is "better"
                            best = v.get_no_of_entries() #count the keys 
                            n =k
        return n 
    
    def find_by_index(self,tmp,idx):
        r = idx.find_rows(tmp)
        res = {}
        for k in r:
            res[k] = self._rows[k]
        return res
    
    def find_by_scan_template(self,tmp,rows):
        result = []
        for k,v in rows.items():
            if self._matches_template(v,tmp):
                result.append({k:v})
        return result 

    def find_by_template(self, tmp, fields= None, use_index =True):       
        
        if tmp is None:
            new_t = CSVDataTable(table_name = "Derived:" + self._table_name, column_names = self._columns, loadit=False)
            new_t.load_from_rows(rows=self._rows)
            return new_t
        
        result_rows = self.find_by_template_rows(tmp,fields,use_index)

        if fields:
            new_cols = fields
        else:
            new_cols = self._column_names
            
        new_t = CSVDataTable(table_name ="Derived:" + self._table_name, column_names = new_cols,  loadit=False)
        new_t.load_from_rows(rows=result_rows)

        return new_t 
    
    def load_from_rows(self, rows):
        self._rows = rows 

    def find_by_template_rows(self, tmp, fields=None, use_index=True):

        if tmp is None:
            return self._rows
        

        idx = self.get_best_index(tmp)
        
        if idx  is None or use_index == False:
            result = self.find_by_scan_template(tmp,self._rows)
        else:
            idx = self._indexes[idx] 
            res = self.find_by_index(tmp,idx)
            result = self.find_by_scan_template(tmp,res)

        if result:
            final_r = {}
            for r in result:
                if fields is not None:
                    for key,v in r.items():
                        final_new_r= {}
                        final_new_r[key] = {k:v[k] for k in fields}
                else:
                    final_new_r = r
                final_r.update(final_new_r)
            return final_r
        
        else: 
            return None

    def get_index_and_selectivity(self,cols):
        on_template = dict(zip(cols,[None]*len(cols)))
        best= None
        n = self.get_best_index(on_template)

        if n is not None:
            best = len(list(self._rows.keys()))/(self._indexes[n].get_no_of_entries())
        
        return n,best

        
    @staticmethod
    def _get_scan_probe(l_table, r_table, on_fields):

        ###Basically compares the indeses and returns the one with better index
        s_best , s_selective = l_table.get_index_and_selectivity(on_fields)
        r_best, r_selective = r_table.get_index_and_selectivity(on_fields)

        result = l_table, r_table
        if s_best is None and r_best is None:
            result=  l_table, r_table
        elif s_best is None and r_best is not None:
            result= r_table, l_table
        elif s_best is not None and r_best is None:
            result = l_table, r_table
        elif s_best is not None and r_best is not None and s_selective < r_selective:
            result= r_table, l_table
        return result 

    def on_clause_to_where(on_c,r):
        result = {c:r[c] for c in on_c}
        return result 
    
    ###DO THISS
    def _get_specific_where(self,wc):
        result = {}
        if wc is not None:
            for k,v in wc.items():
                kk = k.split(".")
                if len(kk)==1:
                    result[k] = v
                elif kk[0] == self._table_name:
                    result[kk[1]] = v
        if result == {}:
            result = None
        
        return result 
    
    def _get_specific_project(self, p_clause):
        result = []
        if p_clause is not None:
            for k in p_clause:
                kk = k.split(".")
                if len(kk)==1:
                    result.append(k)
                elif kk[0]== self._table_name:
                    result.append(kk[1])
        if result ==[]:
            result = None
        
        return result 

    
    def join(self, r_table, on_clause, w_clause=None, p_clause= None, optimize = True):
        
        """
        
        self in this case is the left table
        on_fields = list of columns that exist in both tables
        where_template = standard_tempalte of the form { col : value, col:value}
        project_fields: project, what columns do I want.

        
        """

        ##pick which should be the scan tablea nd which should be the probe table
        if optimize:
            s_table, p_table = self._get_scan_probe(self,r_table, on_clause)
        else:
            s_table = self
            p_table = r_table

        if s_table != self and optimize:
            print("SWAPPED")
        else:
            print("NOT SWAPPING")

        if optimize:
            s_tmp = s_table._get_specific_where(w_clause)
            s_proj = s_table._get_specific_project(p_clause)
            s_rows = s_table.find_by_template(s_tmp,s_proj)
        
        else:
            s_rows = s_table
        
        scan_rows = s_rows.get_rows()

        result = []

        for r in scan_rows:
            p_where = CSVDataTable.on_clause_to_where(on_clause,r)
            p_project = p_table._get_specific_project(p_clause)

            p_rows = p_table.find_by_template(p_where,p_project)
            p_rows = p_rows.get_rows()

            if p_rows:
                for r2 in p_rows:
                    new_r = {**r,**r2}
                    result.append(new_r)

        tn = "JOIN(" + self._table_name +"," + r_table._table_name + ")"
        final_result = CSVDataTable(table_name = tn, column_names=p_clause, loadit=False)
        final_result.load_from_rows(rows=result)

        ###Apply template to result??? 

        return final_result

    def delete(self, template):
        """

        Deletes all records that match the template.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        res = self.find_by_template_rows(template)
        rows = res 
        
        if rows is not None:
            for k in rows.keys():
                self._remove_row(k)
    
    def _remove_row(self,rid):

        r=self._rows[rid]
        if self._indexes is not None:
            for n,idx in self._indexes.items():
                idx.delete_from_index(r,rid)

        del[self._rows[rid]]