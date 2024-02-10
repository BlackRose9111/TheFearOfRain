#objects can be json or database related. Json objects should be managed by the filemanager class in system
import main


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
        main.DATABASECONTEXT.query(query,values)
        self.id = main.DATABASECONTEXT.cursor.lastrowid

    def delete(self):
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        main.DATABASECONTEXT.query(query,(self.id,))

    def update(self):
        fields = [field for field in self.__dict__.keys() if field != "table_name" and field != "id"]
        values = [getattr(self,field) for field in fields]
        query = f"UPDATE {self.table_name} SET {','.join([f'{field} = %s' for field in fields])} WHERE id = %s"
        main.DATABASECONTEXT.query(query,values + [self.id])

    def less_verbose_string(self):
        return ""


    @staticmethod
    def get(id : int):
        query = f"SELECT * FROM User WHERE id = %s"
        result  = main.DATABASECONTEXT.query_with_single_result(query,(id,))
        if result is None:
            return None
        return User(**result.result)

    @staticmethod
    def get_all():
        query = f"SELECT * FROM User"
        result = main.DATABASECONTEXT.query_with_multiple_results(query,())
        if len(result) == 0:
            return []
        return [User(**row) for row in result.result]

    @staticmethod
    def get_all_where(**kwargs):
        query = f"SELECT * FROM User WHERE {' AND '.join([f'{key} = %s' for key in kwargs.keys()])}"
        result = main.DATABASECONTEXT.query_with_multiple_results(query,tuple(kwargs.values()))
        if len(result) == 0:
            return []
        return [User(**row) for row in result.result]

    @staticmethod
    def get_where(**kwargs):
        query = f"SELECT * FROM User WHERE {' AND '.join([f'{key} = %s' for key in kwargs.keys()])}"
        result = main.DATABASECONTEXT.query_with_single_result(query,tuple(kwargs.values()))
        if result.result is None:
            return None
        return User(**result.result)

    @staticmethod
    def find_or_create(discord_id : str):
        user = User.get_where(discord_id=discord_id)
        if user is None:
            user = User(discord_id=discord_id)
            user.save()
        return user


class RpCharacter(DatabaseModel):
    user_id : int
    name : str
    arcane : int = 100
    age : int = 18
    bio : str
    image : str = None #url
    approved : bool = False
    def __init__(self,**kwargs):
        super().__init__()
        self.table_name = "RpCharacter"
        #set attributes automatically
        for key in kwargs.keys():
            setattr(self,key,kwargs[key])

    def get_user(self):
        return User.get(self.user_id)

    def less_verbose_string(self):
        return f"""{self.name} By <@{self.get_user().discord_id}>"""

    def save(self):
        context = main.DATABASECONTEXT
        fields = [field for field in self.__dict__.keys() if field != "table_name" and field != "id"]
        values = [getattr(self,field) for field in fields]
        query = f"INSERT INTO {self.table_name} ({','.join(fields)}) VALUES ({','.join(['%s' for _ in fields])})"
        context.query(query,values)
        self.id = context.cursor.lastrowid

    def delete(self):
        context = main.DATABASECONTEXT
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        context.query(query,(self.id,))

    def update(self):
        context = main.DATABASECONTEXT
        fields = [field for field in self.__dict__.keys() if field != "table_name" and field != "id"]
        values = [getattr(self,field) for field in fields]
        query = f"UPDATE {self.table_name} SET {','.join([f'{field} = %s' for field in fields])} WHERE id = %s"
        context.query(query,values + [self.id])

    def less_verbose_string(self):
        return f"{self.name} - {self.get_user().discord_id}"

    @staticmethod
    def get(id : int):
        context = main.DATABASECONTEXT
        query = f"SELECT * FROM RpCharacter WHERE id = %s"
        result = context.query_with_single_result(query,(id,))
        if result is None:
            return None
        return RpCharacter(**result.result)

    @staticmethod
    def get_all():
        context = main.DATABASECONTEXT
        query = f"SELECT * FROM RpCharacter"
        result = context.query_with_multiple_results(query,())
        if len(result) == 0:
            return []
        return [RpCharacter(**row) for row in result.result]

    @staticmethod
    def get_all_where(**kwargs):
        context = main.DATABASECONTEXT
        query = f"SELECT * FROM RpCharacter WHERE {' AND '.join([f'{key} = %s' for key in kwargs.keys()])}"
        result = context.query_with_multiple_results(query,tuple(kwargs.values()))
        if len(result) == 0:
            return []
        return [RpCharacter(**row) for row in result.result]

    @staticmethod
    def get_where(**kwargs):
        context = main.DATABASECONTEXT
        query = f"SELECT * FROM RpCharacter WHERE {' AND '.join([f'{key} = %s' for key in kwargs.keys()])}"
        result  = context.query_with_single_result(query,tuple(kwargs.values()))
        if result is None:
            return None
        return RpCharacter(**result.result)

    @staticmethod
    def find_or_create(User_id : int,name : str):
        character = RpCharacter.get_where(User_id=User_id,name=name)
        if character is None:
            character = RpCharacter(User_id=User_id,name=name)
            character.save()
        return character

    @staticmethod
    def get_all_for_user(User_id : int):
        return RpCharacter.get_all_where(User_id=User_id)

    
