from nextcord import ButtonStyle
from nextcord.ui import button,View


class ApproveCharacterButton(View):
    def __init__(self,*, character,action,author,ctx):
        super().__init__(timeout=600)
        self.character = character
        self.action = action
        self.author = author
        self.ctx = ctx
    async def on_timeout(self):
        await self.ctx.send("Timeout")
        self.stop()
    @button(label="Approve",style=ButtonStyle.green)
    async def approve(self,button,interaction):
        #check if the user is the author
        if interaction.user == self.author:
            self.action(character=self.character)
            await interaction.send("Character Approved")
            for child in self.children:
                child.disabled = True
            await interaction.message.edit(view=self)
            self.stop()





