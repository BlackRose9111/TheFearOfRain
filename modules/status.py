from nextcord import Game
from nextcord.ext import tasks
from nextcord.ext.commands import Cog


class Status(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.task = None
        self.current_index = 0
        self.status_options = [
            Game(name="with your heart"),
            Game(name="with your mind"),
            Game(name="with your soul"),
            Game(name="with your life"),
            Game(name="with your future"),
            Game(name="with your past"),
            Game(name="with your present"),
            Game(name="with your destiny"),
            Game(name="with your fate"),
            Game(name="with your dreams"),
            Game(name="with your nightmares"),
            Game(name="with your fears"),
            Game(name="with your hopes"),
            Game(name="with your desires"),
            Game(name="with your wishes"),
            Game(name="with your thoughts"),
            Game(name="with your feelings"),
            Game(name="with your emotions"),
            Game(name="with your memories"),
            Game(name="with your experiences")]




    @Cog.listener()
    async def on_ready(self):
        print("Status Cog is ready")
        self.task = self.change_status.start()


    @tasks.loop(hours=1)
    async def change_status(self):
        await self.bot.change_presence(activity=self.status_options[self.current_index])
        self.current_index += 1
        if self.current_index == len(self.status_options):
            self.current_index = 0




def setup(bot):
    bot.add_cog(Status(bot))

