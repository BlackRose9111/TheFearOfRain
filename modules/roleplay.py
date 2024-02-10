from main import filemanager
from data.objects import User, RpCharacter, DatabaseModel
from datetime import datetime
import pytz
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot, Context


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
    time_zone = pytz.timezone("Etc/GMT+9")
    formatted_time = datetime.now(time_zone).strftime("%H:%M")
    clock_details = filemanager.get_json(alias="config",debug=False)["time"]
    desc = f"""{clock_details["before_text"]} `{formatted_time}`\n{clock_details["after_text"]}
    **Weather:** {filemanager.get_json(alias="config",debug=False)["weather"]}
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

    @commands.command()
    async def characters(self,ctx,member : Member = None):
        if member is None:
            member = ctx.author
        user = User.find_or_create(discord_id=str(member.id))
        characters = RpCharacter.get_all_for_user(User_id=user.id)
        t = f"""{member.mention} has the following characters:\n"""
        for character in characters:
            t += f"{character.name}\n"
        vembed = Embed(title="Characters",description=t,colour=0x00ff00)
        await ctx.send(embed=vembed)




def setup(bot):
    bot.add_cog(Roleplay(bot))

