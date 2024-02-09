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





async def multiplechoices(client : Bot,ctx : Context, list_of_models : list[DatabaseModel]):
    t = f"""Multiple choices found. Please select one of the following by typing the number of the choice:
    """
    increment = 1
    for model in list_of_models:
        t += f"{increment}. {model.less_verbose_string()}\n"
        increment+=1
    vembed = Embed(description=t, colour=0xfa00ff)
    message = await ctx.send(embed=vembed)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await client.wait_for('message', check=check, timeout=30)
        msg = int(msg.content)
        if msg > len(list_of_models):
            raise Exception("Cancelled")
        return list_of_models[msg - 1]
    except:
        await ctx.send("Invalid choice")
        return None

def generate_clock_embed():
    formatted_time = Timemanager().get_time()
    clock_details = filemanager.get_json(alias="config")["time"]
    desc = f"""{clock_details["before_text"]} `{formatted_time}`\n{clock_details["after_text"]}
    """
    embed = Embed(title=clock_details,description=desc,colour=clock_details["color"])
    embed.set_footer(text=clock_details["footer"])
    return embed
