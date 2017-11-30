import inspect

from search_engines.utils.mysql import mysql


class db():
    __db_class = None
    __error = None
    __where = {}

    def __init__(self,mysql_config):
        if self.__db_class is None :
            self.__db_class = mysql(mysql_config)

    def get_db(self):
        return self.__db_class

    def table(self,table_name):
        self.get_db().set_table(table_name)
        self.__where = {}
        return self

    def get_table(self):
        if self.get_db().get_table() is None :
            raise Exception ('db table name is empty!!!')
        return self.get_db().get_table()

    def where(self,data):
        self.__where = data
        return self

    def insert(self,data):
        if isinstance(data,dict) != True:
            raise Exception('data type is not dict')
        try:
            for key in data:
                data[key] = '"'+str(data[key])+'"'
            columns = ','.join(data.keys())
            values  = ','.join(data.values())
            sql = 'insert into ' + self.get_table() + '('+ columns + ') values ' + '(' + values + ')'
            last_insert_id = self.get_db().insert(sql)
            return last_insert_id
        except Exception as e:
            self.set_error(e)
            return False

    def update(self,data,where):
        if isinstance(data,dict) != True:
            raise Exception('data type is not dict')
        if isinstance(where,dict) != True:
            raise Exception('where data type is not dict')
        try:
            fields = ",".join('`'+col+'` = %s' for col in data.keys())
            values = tuple(["'"+str(val)+"'" for val in data.values()])
            set_fields = fields % values

            fields = " and ".join('`'+col+'` = %s' for col in where.keys())
            values = tuple(["'"+str(val)+"'" for val in where.values()])
            where_fields = fields % values
            sql = 'update ' + self.get_table() + ' set %s' % set_fields + ' where ' + where_fields
            self.get_db().update(sql)
            return True
        except Exception as e:
            self.set_error(e)
            return False



    def find(self):
        try:
            if len(self.__where) == 0 :
                return None
            else :
                fields = " and ".join('`'+col+'` = %s' for col in self.__where.keys())
                values = tuple(["'"+str(val)+"'" for val in self.__where.values()])
                where_fields = ' where ' + fields % values

            sql = 'select * from ' + self.get_table() + where_fields
            return self.get_db().find(sql)
        except Exception as e:
            self.set_error(e)

    def find_all(self):
        try:
            if len(self.__where) == 0 :
                return None
            else :
                fields = " and ".join('`'+col+'` = %s' for col in self.__where.keys())
                values = tuple(["'"+str(val)+"'" for val in self.__where.values()])
                where_fields = ' where ' + fields % values

            sql = 'select * from ' + self.get_table() + where_fields
            print(sql)
            return self.get_db().find_all(sql)
        except Exception as e:
            self.set_error(e)

    def query(self,sql):
        try:
            return self.get_db().find_all(sql)
        except Exception as e:
            self.set_error(e)

    def execute(self,sql):
        try:
            return self.get_db().execute(sql)
        except Exception as e:
            self.set_error(e)

    def get_last_insert_id(self):
        try:
            return self.get_db().get_cursor().lastrowid

        except Exception :
            return 0

    def count(self,sql):
        try :
            data = self.get_db().find_all(sql)
            return len(data)
        except Exception as e:
            return 0

    def get_error(self):
        return self.__error

    def set_error(self,error_msg):
        if self.get_error() != None:
            msg = self.get_error()+ '\n'
        else:
            msg = ''
        self.__error = msg + 'error:[function_name : %s]' % inspect.stack()[1][3] + str(error_msg)