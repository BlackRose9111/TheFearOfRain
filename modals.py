from nextcord import TextInputStyle
from nextcord.ui import Modal, TextInput


class CharacterSubmit(Modal):
    def __init__(self,author,action : callable):
        super().__init__(title="Character Submit",timeout=6000)
        self.action = action
        self.author = author
        self.character_name = TextInput(label="Character Name",max_length=150,required=True)
        self.age = TextInput(label="Age",max_length=3,required=True,default_value="18")
        self.bio = TextInput(label="Bio",max_length=2000,required=True,style=TextInputStyle.paragraph,placeholder="You can put a google docs link here.")
        self.image_url = TextInput(label="Image URL",max_length=2000,required=False,placeholder="You can leave this empty.")
        self.add_item(self.character_name)
        self.add_item(self.age)
        self.add_item(self.bio)
        self.add_item(self.image_url)

    async def interaction_check(self,interaction):
        return interaction.user == self.author

    async def callback(self,interaction):
        result = self.action(name=self.character_name.value,age=self.age.value,bio=self.bio.value,member=self.author,image=self.image_url.value)
        if result is None:
            await interaction.send("Something went wrong, please try again.")
        else:
            await interaction.send(f"Character {result.name} submitted. An admin will review it soon. If you want changes done to this character, please let an admin know.")
        self.stop()

