import discord
from discord import app_commands
from discord import ui

# from typing import Coroutine
# from discord.utils import MISSING

from gtts import gTTS
import os
import json
import asyncio

import scripts.dados as dados
import scripts.interfaces as interfaces

dados.FirstRun()

from toke import token

intents = discord.Intents.none()
intents.voice_states = True
intents.guild_messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

comandos = ['zentrar','zair','zparar', 'zhelp']
lUsuarios = []
#region Eventos
@client.event
async def on_ready():
    dados.DefaultConfigs(client)

@client.event
async def on_message(message:discord.Message):
    if message.content == 'comando super secreto':
        for canal in message.guild.text_channels:
            print(canal.name)
    elif message.content == 'comando super mega secreto':
        await message.channel.send(message.author.id)
#endregion

#region Slash Commands
@tree.command(
    name='config', 
    description='Selecione os chats que o bot irá funcionar'
)
async def SlashConfig(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator or interaction.user.id == 548887462475464736:#id da minha conta do discord
        await interaction.response.send_message('Selecione os chats em que o bot funcionará:',view=interfaces.Config(client,interaction.guild),ephemeral=True)
    else:
        await interaction.response.send_message('Você não tem permissão de administrador',ephemeral=True)
    
@tree.command(
        name='canais',
        description='Veja os chats onde o bot funciona'
)
async def SlashCanais(interaction:discord.Interaction):
    with open(dados.PATH_CONFIG) as fileRead:
        jsonFile:dict = json.load(fileRead)

    channels = jsonFile[str(interaction.guild.id)]["canais"]

    if channels == "todos":
        await interaction.response.send_message('O bot funcionará em todos os canais, caso não seja isso que você quer utilize /config', ephemeral=True)
    else:
        string = ""

        for channel in channels:
            string += f"\n{interaction.guild.get_channel(int(channel)).mention}"
        
        if len(channels) == 1:
            await interaction.response.send_message(f'O bot funcionará apenas nesse chat:'+string, ephemeral=True)
        else:
            await interaction.response.send_message(f'O bot funcionará nos seguintes canais:'+string, ephemeral=True)
#endregion

client.run(token)
