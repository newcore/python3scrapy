import inspect
import pymysql

class mysql () :
    __host = ''
    __port = None
    __user = ''
    __passwd = ''
    __db = ''
    __charset = ''
    __conn = None
    __cursor = None
    __error = None
    table_name = None

    def __init__(self,mysql_config):
        self.__host = mysql_config.get('host')
        self.__port = mysql_config.get('port')
        self.__user = mysql_config.get('user')
        self.__passwd = mysql_config.get('passwd')
        self.__db = mysql_config.get('db')
        self.__charset = mysql_config.get('charset')
        self.__conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__passwd, db=self.__db, charset=self.__charset,
                             cursorclass=pymysql.cursors.DictCursor)

    def get_cursor(self):
        if self.__cursor == None :
            self.__cursor = self.__conn.cursor()
        return self.__cursor

    def set_table(self, table_name):
        self.table_name = table_name

    def get_table(self):
        return self.table_name

    def query(self,sql):
        try :
            cursor = self.get_cursor()
            res = cursor.execute(sql)
            return res
        except pymysql.Error as e:
            raise Exception ("Mysql Error:%s\nSQL:%s" %(e,sql))

    def execute(self,sql):
        try :
            self.query(sql)
            self.__conn.commit()
            self.close_conn()
            return True
        except pymysql.Error as e:
            raise Exception ("Mysql Error:%s\nSQL:%s" %(e,sql))

    def find(self,sql):
        try :
            self.query(sql)
            res = self.get_cursor().fetchone()
            self.__conn.commit()
            self.close_conn()
            return res
        except Exception as e:
             raise Exception (e)

    def find_all(self,sql):
        try :
            self.query(sql)
            res = self.get_cursor().fetchall()
            self.close_conn()
            return res
        except Exception as e:
            raise Exception (e)

    def update(self,sql):
        try:
            self.query(sql)
            self.__conn.commit()
            self.close_conn()
            return True
        except Exception as e:
            raise Exception (e)

    def insert(self,sql):
        try:
            self.query(sql)
            last_insert_id =  self.get_cursor().lastrowid
            self.__conn.commit()
            self.close_conn()
            return last_insert_id
        except Exception as e:
            raise Exception (e)

    def close_conn(self):
        self.__cursor.close()
        self.__cursor = None
        # self.__conn.close()

    def get_error(self):
        return self.__error

    def set_error(self,error_msg):
        if self.get_error() != None:
            msg = self.get_error()+ '\n'
        else:
            msg = ''
        self.__error = msg + 'error:[function_name : %s]' % inspect.stack()[1][3] + str(error_msg)




