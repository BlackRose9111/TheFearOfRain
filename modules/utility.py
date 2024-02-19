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

    @ping.error
    async def ping_error(self,ctx,error):
        await ctx.send(f"Error: {error}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def echo(self,ctx,*,message):
        original_message = ctx.message
        await original_message.delete()
        await ctx.send(message)

    @echo.error
    async def echo_error(self,ctx,error):
        await ctx.send(f"Error: {error}")

def setup(bot):
    bot.add_cog(Utility(bot))