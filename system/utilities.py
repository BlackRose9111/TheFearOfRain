from nextcord import Embed
from nextcord.ext.commands import Context, Bot
from system.filemanager import filemanager
import pytz
from data.objects import DatabaseModel
from datetime import datetime

class Timemanager:
    def __init__(self):
        self.timezone = pytz.timezone("Europe/Istanbul")

    def get_time(self):
        return Timemanager.format_time(datetime.now(self.timezone))

    @staticmethod
    def format_time(time):
        #only hours and minutes
        return time.strftime("%H:%M")

    @staticmethod
    def format_seconds(seconds):
        time = seconds
        timesuffix = "S"
        if seconds >= 60:
            time = seconds / 60
            timesuffix = "M"
            if time >= 60:
                time = time / 60
                timesuffix = "H"
                if time >= 24:
                    time = time / 24
                    timesuffix = "D"
                    if time >= 365:
                        time = time / 365
                        timesuffix = "Y"
        return str(round(time,2)) + timesuffix

    @staticmethod
    def get_time_difference(first,second):
        return (first - second).total_seconds()







