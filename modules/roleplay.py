import nextcord

import buttons
from main import filemanager
from data.objects import RpCharacter, DatabaseModel
from datetime import datetime
import pytz
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot, Context
import modals


def approve_character(character : RpCharacter):
    character.approved = True
    character.update()
    #find the user

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

def create_character_callback(name,age,bio,member,image=None):
    character = RpCharacter(name=name,age=age,bio=bio,discord_id=str(member.id),image=image)
    character.create()
    return character

def character_embed(character : RpCharacter):
    icons = (":x:",":white_check_mark:")
    text = f"""**Name:** {character.name}
    
    **Age:** {character.age}
    
    **Bio:** {character.bio}
    
    **Approved:** {icons[int(character.approved)]}
    
    **Arcane:** {character.arcane:,} :star:
    
    **Owner:** <@{character.discord_id}>
    
    """
    embed = Embed(title="Character",description=text,colour=0x00ff00)
    if character.image is not None:
        embed.set_image(url=character.image)
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
        characters = RpCharacter.find_all(discord_id=str(member.id))
        t = f"""{member.mention} has the following characters:\n"""
        for character in characters:
            t += f"{character.name}\n"
        vembed = Embed(title="Characters",description=t,colour=0x00ff00)
        await ctx.send(embed=vembed)


    @characters.error
    async def characters_error(self,ctx,error):
        await ctx.send(error)

    @nextcord.slash_command(name="create_character",description="Submit a character for approval")
    async def submit_character(self,interaction : nextcord.Interaction):
        modal = modals.CharacterSubmit(author=interaction.user,action=create_character_callback)
        await interaction.response.send_modal(modal)

    @submit_character.error
    async def submit_character_error(self,interaction,error):
        await interaction.response.send_message(f"Error: {error}")

    @commands.command()
    async def characterinfo(self,ctx,*,name):
        characters = RpCharacter.find_name_like(name)
        if len(characters) > 1:
            character : RpCharacter = await multiplechoices(self.bot,ctx,characters)
        elif len(characters) == 1:
            character = characters[0]
        else:
            await ctx.send("Character not found")
            return
        if character is not None:
            vembed = character_embed(character)
            if isinstance(ctx.author, Member):
                if ctx.author.guild_permissions.administrator and not bool(character.approved):
                    view = buttons.ApproveCharacterButton(character=character, action=approve_character,
                                                          author=ctx.author, ctx=ctx)
                    await ctx.send(embed=vembed, view=view)
                    return
            await ctx.send(embed=vembed)

    @characterinfo.error
    async def characterinfo_error(self,ctx,error):
        await ctx.send(error)

    @commands.command(brief="Allow Through Lobby",description="Allow a user through the lobby")
    @commands.has_permissions(administrator=True,manage_guild=True)
    async def allowthroughlobby(self,ctx,member : Member):
        role = nextcord.utils.get(ctx.guild.roles,name="Lobby")
        role_to_give = nextcord.utils.get(ctx.guild.roles,name="Member")
        await member.remove_roles(role)
        await member.add_roles(role_to_give)
        await ctx.send(f"{member.mention} allowed through the lobby")

    @allowthroughlobby.error
    async def allowthroughlobby_error(self,ctx,error):
        await ctx.send(error)


    @commands.command(brief="Edit the properties of a character",description="Edit the properties of a character. Fields can be name,age,bio,image,approved,arcane,discord_id")
    @commands.has_permissions(administrator=True,manage_guild=True)
    async def editcharacter(self,ctx,character_name,field,*,value):
        characters = RpCharacter.find_name_like(character_name)
        if len(characters) > 1:
            character : RpCharacter = await multiplechoices(self.bot,ctx,characters)
        else:
            character = characters[0]
        if character is None:
            await ctx.send("Character not found")
            return
        match(field.lower()):
            case "name":
                character.name = value
            case "age":
                character.age = int(value.replace(" ","").replace(",",""))
            case "bio":
                character.bio = value
            case "image":
                character.image = value
            case "approved":
                def text_to_bool(text):
                    if text.lower in ("true","yes","1","approved","accept"):
                        return True
                    return False
                character.approved = text_to_bool(value)
            case "arcane":
                character.arcane = int(value.replace(" ","").replace(",",""))

            case "discord_id":
                character.discord_id = value
            case _:
                await ctx.send("Invalid field")

        character.update()
        await ctx.send(f"Character {field.lower()} updated to {value}")

    @editcharacter.error
    async def editcharacter_error(self,ctx,error):
        await ctx.send(error)

    @commands.command(brief="Delete a character",description="Delete a character from the database")
    @commands.has_permissions(administrator=True,manage_guild=True)
    async def deletecharacter(self,ctx,*,name):
        characters = RpCharacter.find_name_like(name)
        character : RpCharacter = await multiplechoices(self.bot,ctx,characters)
        if character is None:
            await ctx.send("Character not found")
            return
        character.delete()
        await ctx.send(f"Character {character.name} deleted")

    @deletecharacter.error
    async def deletecharacter_error(self,ctx,error):
        await ctx.send(error)

    @commands.command(brief="Characters Not Approved",description="List all characters that are not approved")
    @commands.has_permissions(administrator=True,manage_guild=True)
    async def charactersnotapproved(self,ctx):
        characters = RpCharacter.find_all(approved=False)
        t = "The following characters are not approved:\n"
        for character in characters:
            t += f"{character.name} by <@{character.discord_id}>\n"
        vembed = Embed(title="Characters Not Approved",description=t,colour=0x00ff00)
        await ctx.send(embed=vembed)

    @charactersnotapproved.error
    async def charactersnotapproved_error(self,ctx,error):
        await ctx.send(error)





def setup(bot):
    bot.add_cog(Roleplay(bot))

