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

@client.event
async def on_ready():
    dados.DefaultConfigs(client)

    

@client.event
async def on_message(message:discord.Message):
    if message.content == 'comando super secreto':
        for canal in message.guild.text_channels:
            print(canal.name)
        

@tree.command(
    name='config', 
    description='Selecionar o canal que o bot irá funcionar'
)
async def SlashConfig(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator or interaction.user.name == "zagz.":
        await interaction.response.send_message('Selecione os chats em que o bot funcionará:',view=interfaces.NewConfig(client,interaction.guild),ephemeral=True)
    
    else:
        await interaction.response.send_message('Você não tem permissão de administrador',ephemeral=True)
    



client.run(token)
