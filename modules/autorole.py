from nextcord import Embed
from nextcord.ext.commands import Cog

from data.objects import RpCharacter


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
            embed = Embed(title="Welcome",description=f"Welcome to the server {member.mention}\n Please submit a character and wait for approval before gaining access to the rest of the server.",colour=0x00ff00)
            channel = member.guild.get_channel(1205483966094647376)
            await channel.send(embed=embed)
            print(f"Gave {member} the role {role}")
        except Exception as e:
            print(f"An exception occured {e}")

    @Cog.listener()
    async def on_member_remove(self, member):
        print("Member left")
        try:
            channel = member.guild.get_channel(1205483966094647376)
            vembed = Embed(title="Goodbye",description=f"{member.display_name()} has left the server.",colour=0xff0000)
            await channel.send(embed=vembed)
            list_characters = RpCharacter.find_all(discord_id=str(member.id))
            t = f"{member.mention} has left the server. The following characters have been archived:\n"
            for character in list_characters:
                character.approved = False
                character.update()
                t += f"{character.name}\n"
            vembed = Embed(title="Characters Archived",description=t,colour=0x00ff00)
            await channel.send(embed=vembed)


        except Exception as e:
            print(f"An exception occured {e}")

def setup(bot):
    bot.add_cog(Autorole(bot))