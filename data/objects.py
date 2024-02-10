#objects can be json or database related. Json objects should be managed by the filemanager class in system
import main

class ItemAlreadyExists(Exception):
    def __init__(self):
        super().__init__("Item already exists")

class ItemDoesNotExist(Exception):
    def __init__(self):
        super().__init__("Item does not exist")



class DatabaseModel:

    id : int = None
    table_name : str = None
    def __init__(self):
        pass

    # C R U D
    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def find(*,id : int = None, **kwargs):
        pass

    @staticmethod
    def find_all(**kwargs):
        pass

    @staticmethod
    def find_or_create(**kwargs):
        pass

    def less_verbose_string(self):
        return str(self.id)

    def __str__(self):
        return str(self.__dict__)


class RpCharacter(DatabaseModel):
    name : str = None
    age : int = 18
    bio : str = None
    arcane : int = 100
    discord_id : str = None
    approved : bool = False
    image : str = None
    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs.keys():
            setattr(self,key,kwargs[key])

    def less_verbose_string(self):
        return f"{self.name}"

    def __str__(self):
        icons = (":x:",":white_check_mark:")
        return f"{self.name} - {icons[int(self.approved)]}"
    def create(self):
        if self.id is not None:
            raise ItemAlreadyExists
        else:
            query_string = "INSERT INTO RpCharacter (name,age,bio,arcane,discord_id,approved,image) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            main.DatabaseCursor.execute(query_string,(self.name,self.age,self.bio,self.arcane,self.discord_id,self.approved,self.image))
            main.DatabaseConnection.commit()
            self.id = main.DatabaseCursor.lastrowid



    def update(self):
        if self.id is None:
            raise ItemDoesNotExist
        else:
            query_string = "UPDATE RpCharacter SET "
            params = []
            for key in self.__dict__.keys():
                if key != "id":
                    query_string += f"{key} = %s,"
                    params.append(self.__dict__[key])
            query_string = query_string[:-1]
            query_string += " WHERE id = %s"
            params.append(self.id)
            main.DatabaseCursor.execute(query_string,params)
            main.DatabaseConnection.commit()

    def delete(self):
        if self.id is None:
            raise ItemDoesNotExist
        else:
            main.DatabaseCursor.execute("DELETE FROM RpCharacter WHERE id = %s",(self.id,))
            main.DatabaseConnection.commit()
            self.id = None

    @staticmethod
    def find(*,id : int = None, **kwargs):
        query_string = "SELECT * FROM RpCharacter WHERE "
        params = []
        if id is not None:
            query_string += "id = %s"
            params.append(id)
        else:
            for key in kwargs.keys():
                query_string += f"{key} = %s AND "
                params.append(kwargs[key])
            query_string = query_string[:-5]
        main.DatabaseCursor.execute(query_string,params)
        #cursor returns a dictionary
        result = main.DatabaseCursor.fetchone()
        if result is None:
            return None
        else:
            return RpCharacter(**result)

    @staticmethod
    def find_all(**kwargs):
        query_string = "SELECT * FROM RpCharacter WHERE "
        params = []
        for key in kwargs.keys():
            query_string += f"{key} = %s AND "
            params.append(kwargs[key])
        query_string = query_string[:-5]
        main.DatabaseCursor.execute(query_string,params)
        result = main.DatabaseCursor.fetchall()
        if result is None:
            return None
        else:
            return [RpCharacter(**item) for item in result]

    @staticmethod
    def find_name_like(name):
        query_string = "SELECT * FROM RpCharacter WHERE name LIKE %s"
        main.DatabaseCursor.execute(query_string,("%"+name+"%",))
        result = main.DatabaseCursor.fetchall()
        if result is None:
            return None
        else:
            return [RpCharacter(**item) for item in result]

