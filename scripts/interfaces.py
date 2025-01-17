import discord
from discord import ui

from scripts.dados import UpdateChannels

def GetOptionsByGuild(guild: discord.Guild) -> list[discord.SelectOption]:
    options = []
    for channel in guild.text_channels:
        option = discord.SelectOption(label=channel.name,value=str(channel.id))
        options.append(option)
    
    return options

class Config(ui.View):
    
    def __init__(self, client: discord.Client, guild:discord.Guild):
        super().__init__()
        self.guild = guild

        self.StartSelect()
        self.StartButton()

    def StartSelect(self):
        options = GetOptionsByGuild(self.guild)

        select = ui.Select(options= options, max_values=len(options))
        async def SelectCallback(interaction: discord.Interaction):
            UpdateChannels(interaction.guild.id, select.values)
            if len(select.values) == 1:
                await interaction.response.send_message(f'O bot funcionará no chat {interaction.guild.get_channel(int(select.values[0])).mention}', ephemeral=True)
            else:
                string = ""
                for channel in select.values:
                    string += f"\n{interaction.guild.get_channel(int(channel)).mention}"
                await interaction.response.send_message('O bot funcionará nos seguintes chats:'+string,ephemeral=True)

            print(f'A configuração do servidor {interaction.guild.name} de id {interaction.guild_id} foi setada para os canais de id: {select.values}')

        select.callback = SelectCallback

        self.add_item(select)

    def StartButton(self):
        
        button = ui.Button(label='Todos os chats',style=discord.ButtonStyle.blurple)
        async def ButtonCallback(interaction:discord.Interaction):
            UpdateChannels(interaction.guild.id)
            await interaction.response.send_message("Agora o bot funciona em todos os canais",ephemeral=True)
            print(f'A configuração do servidor {interaction.guild.name} de id {interaction.guild_id} foi setada para todos os canais')

        button.callback = ButtonCallback

        self.add_item(button)