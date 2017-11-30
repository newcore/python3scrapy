import time


class log ():
    def __init__(self):
        pass


    def add_log(self,file_name,content):
        try:
            with open(file_name,'w') as f:
                date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                content = date,content,"\r\n"
                f.write(content)
                f.close()
        except Exception as e:
            raise Exception (e)