from nextcord.ext.commands import Cog


class Utility(Cog):

    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        print("Utility Cog is ready")


def setup(bot):
    bot.add_cog(Utility(bot))