from nextcord import Embed
from nextcord.ext.commands import Cog


class Autorole(Cog):

    def __init__(self, bot):
        self.bot = bot
    @Cog.listener()
    async def on_ready(self):
        print("Autorole Cog is ready")

    @Cog.listener()
    async def on_member_join(self, member):
        print("Member joined")
        try:
            role = member.guild.get_role(1205479230322778134)
            await member.add_roles(role)

            embed = Embed(title="Welcome",description=f"Welcome to the server {member.mention}",colour=0x00ff00)
            channel = member.guild.get_channel(1205483966094647376)
            await channel.send(embed=embed)
            print(f"Gave {member} the role {role}")
        except Exception as e:
            print(f"An exception occured {e}")



def setup(bot):
    bot.add_cog(Autorole(bot))