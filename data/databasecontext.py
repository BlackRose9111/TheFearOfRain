#manage your database connections here, low level actions only
import mysql.connector

class DatabaseQueryResult:
    def __init__(self,result,id : int):
        self.result = result
        self.id = id

    def __getitem__(self, item):
        return self.result[item]

    def __len__(self):
        return len(self.result)


class DatabaseContext:
    def __init__(self,connection):
        self.connection : mysql.connector.MySQLConnection = connection
        self.cursor = self.connection.cursor(buffered=True,dictionary=True)

    def keepalive(self):
        self.connection.ping(reconnect=True)

    def close(self):
        self.connection.close()

    def query(self,query_string : str,params : tuple):
        self.cursor.execute(operation= query_string,params=params)

    def query_with_single_result(self,query_string : str,params : tuple):
        self.cursor.execute(operation= query_string,params=params)
        return DatabaseQueryResult(result=self.cursor.fetchone(),id=self.cursor.lastrowid)

    def query_with_multiple_results(self,query_string : str,params : tuple):
        self.cursor.execute(operation= query_string,params=params)
        return DatabaseQueryResult(result=self.cursor.fetchall(),id=self.cursor.lastrowid)




