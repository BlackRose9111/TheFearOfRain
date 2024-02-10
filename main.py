import nextcord
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from nextcord.ext import commands,tasks

import os
import mysql.connector
import json
import mysql.connector




class filemanager():
    aliases : dict = {"alias": "variables/config/aliases.json"}
    def __init__(self):
        self.get_aliases()

    def get_aliases(self):
        obj : dict = filemanager.get_json(address=self.aliases["alias"],debug=False)
        for key in obj.keys():
            self.aliases[key] = obj[key]
    def get_alias(self,alias):
        try:
            return self.aliases[alias]
        except:
            return None


    @staticmethod
    def get_json(*, address : str = None,alias : str = None,debug = True) -> dict or None:
        file_address = None

        try:
            if address is not None:
                file_address = address
            elif address is None and alias is not None:
                fm = filemanager()
                file_address = fm.get_alias(alias=alias)
            elif address is None and alias is None:
                raise Exception("Missing address and alias")
            with open(file_address,"r") as f:
                contents = f.read()
                _object = dict(json.loads(contents))
                if debug is True:
                    print(f"Accessed {file_address}")
                return _object

        except:
            return None
    @staticmethod
    def enter_json(*, dictionary : dict, address :str = None, alias : str = None, debug = True):
        file_address = None
        try:
            if address is not None:
                file_address = address
            elif address is None and alias is not None:
                fm = filemanager()
                file_address = fm.get_alias(alias)
            elif address is None and alias is None:
                raise Exception("Missing address and alias")
            with open(file_address,"w") as f:
                json.dump(dictionary,f)
            if debug is True:
                print(f"Wrote {dictionary} on {file_address}")
        except Exception as e:
            print(f"An exception as occued {e}")

    @staticmethod
    def get_value_from_json(*, key : str, address : str = None,alias : str = None, debug = True,default = None) -> object or None:
        obj = filemanager.get_json(address=address, alias=alias, debug=debug)
        try:
            return obj[key]
        except:
            return default

    @staticmethod
    def change_or_add_value_on_json(*, key : str, new_value, address : str = None, alias : str = None, debug =True):
        obj = filemanager.get_json(address=address, alias=alias, debug=debug)
        obj[key] = new_value
        filemanager.enter_json(dictionary=obj,address=address,alias=alias,debug=debug)

    @staticmethod
    def delete_value_on_json(*, key : str, address : str  = None,alias : str = None, debug = True):
        obj : dict = filemanager.get_json(address=address,alias=alias,debug=debug)
        obj.pop(__key=key)
        filemanager.enter_json(dictionary=obj,address=address,alias=alias,debug=debug)




owner_ids = [240027656949596160, 1068287199688278166]
bot_name = "Luna"
bot_time_zone = "Europe/Istanbul"
bot = commands.AutoShardedBot(command_prefix="!",
                              strip_after_prefix=True,
                              case_insensitive=True,
                              intents=nextcord.Intents.all(),
                              owner_ids=owner_ids)


run_time = 0
TOKEN = ""
DatabaseConnection :  MySQLConnectionAbstract = None
DatabaseCursor : MySQLCursorAbstract = None

@bot.event
async def on_ready():
    print("Director launched")
    parallel_loop.start()
    database_connect()


def database_connect():
    dbinfo = filemanager.get_json(alias="database",debug=False)
    try:
        connection = mysql.connector.connect(host=dbinfo["host"],
                                             user=dbinfo["user"],
                                             password=dbinfo["password"],
                                             database=dbinfo["database"])
        connection.autocommit = True
        global DatabaseConnection
        DatabaseConnection = connection
        global DatabaseCursor
        DatabaseCursor = connection.cursor(dictionary=True,buffered=True)
    except Exception as e:
        print(f"Failed to connect to database with error {e}")
        DATABASECONTEXT = None



def database_keepalive():
    try:
        DatabaseConnection.ping(reconnect=True,attempts=3, delay=5)
    except:
        pass


@tasks.loop(seconds=1)
async def parallel_loop():
    global run_time
    run_time += 1
    database_keepalive()


def get_token():
    global TOKEN
    try:
        TOKEN = filemanager.get_value_from_json(key="token",alias="token",debug=False)
        if TOKEN is None:
            raise Exception("Token is None")
    except:
        TOKEN = None

    if TOKEN is None:
        while True:
            a = input("Bot Token was not found, please enter it by hand:")
            if a is not None and a != "":
                TOKEN = a
                print("Token entered successfully")
                filemanager.change_or_add_value_on_json(new_value=TOKEN,alias="token",debug=True,key="token")
                break


def load_module(modulename):
    try:
        bot.load_extension(modulename)
    except Exception as e:
        print(f"Failed to load module {modulename} with error {e}")


def load_all_modules():
    for file in os.listdir("modules"):
        #if ends with .py
        if file.endswith(".py"):
            load_module(f"modules.{file[:-3]}")
            print(f"Loaded module {file[:-3]}")


get_token()
load_all_modules()
bot.run(TOKEN)
print("Goodbye! <3")




