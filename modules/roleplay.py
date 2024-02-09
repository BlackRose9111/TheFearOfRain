from datetime import datetime
import pytz
from nextcord import Embed
from system.filemanager import filemanager
from nextcord.ext import commands
from nextcord.ext.commands import Cog

def generate_clock_embed():
    time_zone = pytz.timezone("Etc/GMT+9")
    formatted_time = time_zone.localize(datetime.now()).strftime("%H:%M")
    clock_details = filemanager.get_json(alias="config")["time"]
    desc = f"""{clock_details["before_text"]} `{formatted_time}`\n{clock_details["after_text"]}
    
    Weather: {filemanager.get_json(alias="config")["weather"]}
    """
    embed = Embed(title=clock_details["title"],description=desc,colour=clock_details["color"])
    embed.set_footer(text=clock_details["footer"])
    return embed



class Roleplay(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Roleplay Cog is ready")


    @commands.command(description="Will display the current roleplay time",brief="Will display the time")
    async def time(self,ctx):
        vembed = generate_clock_embed()
        await ctx.send(embed=vembed)

    @time.error
    async def time_error(self,ctx,error):
        await ctx.send(f"Error: {error}")

    @commands.command()
    async def test(self,ctx):
        tm = filemanager.get_json(alias="config")["time"]
        await ctx.send(tm)

    @test.error
    async def test_error(self,ctx,error):
        await ctx.send(error)

    @commands.command()
    async def weather(self,ctx):
        weather = filemanager.get_json(alias="config")["weather"]
        await ctx.send(f"The weather is {weather}")

    @weather.error
    async def weather_error(self,ctx,error):
        await ctx.send(error)

    @commands.command()
    @commands.has_permissions(administrator=True,manage_guild=True)
    async def set_weather(self,ctx,*,weather):
        filemanager.change_or_add_value_on_json(key="weather",alias="config",new_value=weather,debug=False)
        await ctx.send(f"Changed the weather to {weather}")

    @set_weather.error
    async def set_weather_error(self,ctx,error):
        await ctx.send(error)
        

def setup(bot):
    bot.add_cog(Roleplay(bot))

