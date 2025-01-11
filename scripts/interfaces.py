import discord
from discord import ui
import json

def GetOptionsByGuild(guild: discord.Guild) -> list[discord.SelectOption]:
    options = []
    for channel in guild.text_channels:
        option = discord.SelectOption(label=channel.name,value=str(channel.id))
        options.append(option)
    
    return options
        

class NewConfig(ui.View):
    
    def __init__(self, client: discord.Client, guild:discord.Guild):
        super().__init__()
        self.guild = guild

        self.StartSelect()
        self.StartButton()

    def StartSelect(self):
        options = GetOptionsByGuild(self.guild)

        select = ui.Select(options= options, max_values=len(options))
        async def SelectCallback(interaction: discord.Interaction):
            print("Lista de id's selecionados: ",select.values)
        select.callback = SelectCallback

        self.add_item(select)

    def StartButton(self):
        button = ui.Button(label='Todos os chats',style=discord.ButtonStyle.blurple)
        async def ButtonCallback(self, interaction:discord.Interaction, button: ui.Button):
            pass    
        button.callback = ButtonCallback

        self.add_item(button)

class Config(ui.View):
    def __init__(self, client:discord.Client):
        self.client = client
        super().__init__()
# ,min_values=0,max_values=25
    @ui.select(cls=ui.ChannelSelect,channel_types=[discord.ChannelType.text, discord.ChannelType.private])
    
    async def canais(self, interaction:discord.Interaction, canal:ui.ChannelSelect):
        lista = []
        listaJSON = []

        for valores in canal.values:
            chanel = self.client.get_channel(valores.id)
            listaJSON.append(str(chanel.id))
            lista.append(chanel.mention)
        
        with open('config.json', 'r') as arquivo_leitura:
            dados = json.load(arquivo_leitura)

        dados.update({str(interaction.guild.id): listaJSON})

        with open('config.json', 'w') as arquivo_escrita:
            
            json.dump(dados, arquivo_escrita, indent=4)
            print("dados atualizados")




        string = str(lista).replace('[','').replace(',',' ').replace("'",'').replace(']','')
        
        await interaction.response.send_message(content="Canais em que o bot funcionará\n"+ string, ephemeral=True)
        
        
    @ui.button(label='Todos os chats',style=discord.ButtonStyle.blurple)

    async def todos(self, interaction:discord.Interaction, button: ui.Button):
        with open('config.json', 'r') as fileread:
            dados = json.load(fileread)

        dados.update({str(interaction.guild.id):"todos"})

        with open('config.json', 'w') as filewrite:
            json.dump(dados,filewrite,indent=4)
        await interaction.response.send_message('Agora o bot funcionará em todos os canais', ephemeral=True)
