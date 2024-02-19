from nextcord import Member, User
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

    #kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member : Member,*,reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.display_name} has been kicked from the server")

    @kick.error
    async def kick_error(self,ctx,error):
        await ctx.send(f"Error: {error}")

    #ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx,user : User,*,reason="No reason provided"):
        await ctx.guild.ban(user,reason=reason)
        await ctx.send(f"{user.display_name} has been banned from the server")

    @ban.error
    async def ban_error(self,ctx,error):
        await ctx.send(f"Error: {error}")

    #ban by user id if the user is not in the server

def setup(bot):
    bot.add_cog(Utility(bot))