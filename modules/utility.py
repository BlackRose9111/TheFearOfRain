from nextcord.ext import commands
from nextcord.ext.commands import Cog


class Utility(Cog):

    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        print("Utility Cog is ready")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send("Pong")



def setup(bot):
    bot.add_cog(Utility(bot))