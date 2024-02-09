#objects can be json or database related. Json objects should be managed by the filemanager class in system
from main import DATABASECONTEXT as context
from data.databasecontext import DatabaseContext, DatabaseQueryResult
class DatabaseModel:
    id : int
    table_name : str
    def __init__(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def less_verbose_string(self):
        pass

    @staticmethod
    def get(id : int):
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def get_all_where(**kwargs):
        pass

    @staticmethod
    def get_where(**kwargs):
        pass



class User(DatabaseModel):

    discord_id : str
    currency : int = 100
    currency_bank : int = 1000

    def __init__(self,**kwargs):
        super().__init__()
        self.table_name = "User"
        #set attributes automatically
        for key in kwargs.keys():
            setattr(self,key,kwargs[key])

    def save(self):
        fields = [field for field in self.__dict__.keys() if field != "table_name" and field != "id"]
        values = [getattr(self,field) for field in fields]
        query = f"INSERT INTO {self.table_name} ({','.join(fields)}) VALUES ({','.join(['%s' for _ in fields])})"
        context.query(query,values)
        self.id = context.cursor.lastrowid

    def delete(self):
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        context.query(query,(self.id,))

    def update(self):
        fields = [field for field in self.__dict__.keys() if field != "table_name" and field != "id"]
        values = [getattr(self,field) for field in fields]
        query = f"UPDATE {self.table_name} SET {','.join([f'{field} = %s' for field in fields])} WHERE id = %s"
        context.query(query,values + [self.id])

    def less_verbose_string(self):
        return ""

    def take_currency(self,amount : int):
        if self.currency >= amount:
            self.currency -= amount
            self.update()
            return True
        return False
    def give_currency(self,amount : int):
        self.currency += amount
        self.update()
        return True

    def take_currency_bank(self,amount : int):
        if self.currency_bank >= amount:
            self.currency_bank -= amount
            self.update()
            return True
        return False
    def give_currency_bank(self,amount : int):
        self.currency_bank += amount
        self.update()
        return True

    @staticmethod
    def get(id : int):
        query = f"SELECT * FROM User WHERE id = %s"
        result : DatabaseQueryResult = context.query_with_single_result(query,(id,))
        if result is None:
            return None
        return User(**result.result)

    @staticmethod
    def get_all():
        query = f"SELECT * FROM User"
        result : DatabaseQueryResult = context.query_with_multiple_results(query,())
        if len(result) == 0:
            return []
        return [User(**row) for row in result.result]

    @staticmethod
    def get_all_where(**kwargs):
        query = f"SELECT * FROM User WHERE {' AND '.join([f'{key} = %s' for key in kwargs.keys()])}"
        result : DatabaseQueryResult = context.query_with_multiple_results(query,tuple(kwargs.values()))
        if len(result) == 0:
            return []
        return [User(**row) for row in result.result]

    @staticmethod
    def get_where(**kwargs):
        query = f"SELECT * FROM User WHERE {' AND '.join([f'{key} = %s' for key in kwargs.keys()])}"
        result : DatabaseQueryResult = context.query_with_single_result(query,tuple(kwargs.values()))
        if result is None:
            return None
        return User(**result.result)

    @staticmethod
    def find_or_create(discord_id : str):
        user = User.get_where(discord_id=discord_id)
        if user is None:
            user = User(discord_id=discord_id)
            user.save()
        return user



