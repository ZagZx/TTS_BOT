#BUGS PARA ARRUMAR: 
#1° quando o bot é kickado da call o nome do "dono" não é removido da lista
#2° quando o bot é movido da call também acontece o mesmo


import discord
from discord import app_commands
from discord import ui

from typing import Coroutine
from discord.utils import MISSING

from gtts import gTTS
import os
import json

from toke import token



idioma = 'pt'

intents = discord.Intents.all()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

comandos = ['zentrar','zair','zparar', 'zhelp']

lpessoas = []

class Config(ui.View):
    def __init__(self):
        super().__init__()

    @ui.select(cls=ui.ChannelSelect,min_values=0,max_values=25,channel_types=[discord.ChannelType.text, discord.ChannelType.private])
    
    async def canais(self, interaction:discord.Interaction, canal:ui.ChannelSelect):
        lista = []
        listaJSON = []

        for valores in canal.values:
            chanel = client.get_channel(valores.id)
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

@client.event

async def on_ready():
    print(f'Estou online com o nome de {client.user}')
    await tree.sync()

@tree.command(
        name='config', 
        description='Selecionar o canal que o bot irá funcionar'
)

async def config(interaction: discord.Interaction):

    if interaction.user.guild_permissions.administrator or interaction.user.name == "zagz.":
        await interaction.response.send_message('Selecione os chats em que o bot funcionará:',view=Config(),ephemeral=True)
    
    else:
        await interaction.response.send_message('Você não tem permissão de administrador',ephemeral=True)
    

@tree.command(
        name='gremio',
        description='Apoie o grêmio!'
)

async def gremio(interaction: discord.Interaction):
    with open('config.json', 'r') as filer:
        canais = json.load(filer)
    
    serverid = str(interaction.guild.id)
    user = interaction.user.name

    if str(interaction.channel.id) in canais[serverid]:

        with open('apoiadores.json', 'r') as filer:
            apoiadores = json.load(filer)
        
        
        if serverid not in apoiadores:
            apoiadores.update({serverid:[user]})

        if user not in apoiadores[serverid]:
            apoiadores[serverid].append(user)
        
        with open('apoiadores.json', 'w') as filew:
            json.dump(apoiadores,filew, indent=4)

        await interaction.response.send_message(f'{interaction.user.mention} Apoiou o grêmio!')
        
        if interaction.user.voice != None: #and discord.VoiceClient(client,client.get_channel(interaction.user.voice.channel.id)).guild.voice_client in client.voice_clients: #and interaction.user.voice in client.voice_clients:
        
            chanel = client.get_channel(interaction.user.voice.channel.id)
            voice = discord.VoiceClient(client,chanel).guild.voice_client
            if voice in client.voice_clients:
                voice.play(discord.FFmpegPCMAudio('gremio.mp3'))
    else:
        await interaction.response.send_message('Utilize esse comando em canais onde o bot tem permissão para mandar mensagens (/canais)',ephemeral=True)
@tree.command(
        name='canais',
        description='Canais onde o bot funciona'
)

async def canais(interaction:discord.Interaction):
    listach = []
    with open('config.json', 'r') as filer:
        dados = json.load(filer)
    
    
    if dados[str(interaction.guild.id)] != "todos":
        for canal in dados[str(interaction.guild.id)]:
            aux = client.get_channel(int(canal))
            listach.append(aux.mention)
        listach = str(listach)
        listach = listach.replace('[', '').replace("'", '').replace(',','').replace(']','')
    
        await interaction.response.send_message(f'O bot funciona nos seguintes canais\n{listach}', ephemeral=True)
    
    else:
        await interaction.response.send_message('O bot funcionará em todos os canais, caso não seja isso que você quer utilize /config', ephemeral=True)

@tree.command(
        name='apoiadores',
        description='Veja quem apoiou o grêmio'
)

async def apoio(interaction:discord.Interaction):

    with open('config.json','r') as fileread:
        dados = json.load(fileread)
    try:
        if str(interaction.channel.id) in dados[str(interaction.guild.id)]:
            serverid = str(interaction.guild.id)
            with open('apoiadores.json','r') as filer:
                apoiadores = json.load(filer)
            
            apoiadores = str(apoiadores[serverid]).replace('[', '').replace(']','').replace("'", '')

            await interaction.response.send_message(f'Esses são os apoiadores do grêmio :sunglasses:\n**{apoiadores}**')
        else:
            await interaction.response.send_message('Utilize esse comando em canais onde o bot tem permissão para mandar mensagens (/canais)',ephemeral=True)
    except KeyError:
        await interaction.response.send_message('Ninguém apoiou o grêmio ainda :sob:')
@client.event
#configuração padrão ao entrar no servidor

async def on_guild_join(guild:discord.Guild):
    with open('config.json', 'r') as filer:
        dados = json.load(filer)

    dados.update({str(guild.id):"todos"})

    with open('config.json', 'w') as filew:
        json.dump(dados,filew, indent=4)

@client.event

async def on_guild_remove(guild:discord.Guild):
    with open('config.json', 'r') as filer:
        dados = json.load(filer)

    dados.pop(str(guild.id))

    with open('config.json', 'w') as filew:
        json.dump(dados, filew, indent=4)
@client.event
#arrumar bugs quando o servidor do bot cai

async def on_connect():
    global lpessoas

    if lpessoas and client.voice_clients:
        lpessoas = []
        for a in client.voice_clients:
            await a.disconnect(force=True)
        print(lpessoas)

@client.event

async def on_message(message: discord.Message):
    global comandos
    global lpessoas


    

    with open('config.json', 'r') as file:
        lcanais = json.load(file)
    #print(lcanais)
    #print(message.channel.id)
    #print(message.channel.guild.id)
    if message.guild != None and message.channel != None:
        if str(message.channel.id) in lcanais[str(message.guild.id)] or "todos" in lcanais[str(message.guild.id)]: 
            if message.author != client.user and not message.attachments:
                    if message.author.voice != None:
                        chanel = client.get_channel(message.author.voice.channel.id)
                        guild = discord.VoiceClient(client,chanel).guild
                            
                        voice = discord.VoiceClient(client,chanel).guild.voice_client
                        arquivo = (f'audios/{guild}.mp3')
                    
                        try:
                            if message.content.startswith('zentrar'): #MUDAR DEPOIS
                                await chanel.connect(self_deaf=True)
                                await message.channel.send(f'Entrei em {chanel.mention}')
                                lpessoas.append(message.author.name)
                                print(lpessoas)
                        except:
                            await message.channel.send(f'{message.author.mention} Já estou em uma call')
                        if message.author.name in lpessoas and message.content.startswith('zair'): #MUDAR DEPOIS
                        
                            await voice.disconnect(force=True)
                            await message.channel.send('Tá bom já tô indo :C')

                            lpessoas.remove(message.author.name)
                            print(lpessoas)
                            if os.path.exists(arquivo):
                                os.remove(arquivo)
                        elif message.author.name not in lpessoas and message.content.startswith('zair'): #MUDAR DEPOIS
                            await message.channel.send(f'{message.author.mention} Você não tem permissão!')
                            
                        if message.author.name in lpessoas and message.content.startswith('zparar'):
                            voice.stop()
                        elif message.author.name not in lpessoas and message.content.startswith('zparar'):
                            await message.channel.send(f'{message.author.mention} Você não tem permissão!')

                        if message.author.name in lpessoas and not any(message.content == a for a in comandos):  
                            gTTS(text=message.content,lang=idioma,slow=True).save(arquivo)
                            source = discord.FFmpegPCMAudio(source= arquivo)
                            voice.play(source)
                    elif message.content in comandos:
                        await message.channel.send('Você precisa estar conectado em uma call')

                    if message.content.startswith('zhelp'): #or client.user.mentioned_in(message) and not message.mention_everyone:
                        await message.channel.send('''             
        **Comandos**
        zentrar - Entrar na call que você está conectado
        zair - Sair da call
        zparar - parar o áudio tocando                                                                          

        **Informações**
        Apenas quem digitou o comando "zentrar" pode controlar o bot(fazer falar, mandar sair da call e parar o áudio)  
                                                                                    
        Para falar com o bot só é necessário ter utilizado o comando "zentrar" e então digitar normalmente em um chat
                                            ''')
            
@client.event

async def on_voice_state_update(member, before, after):
    
    if before.channel != after.channel and member.name in lpessoas: #aqui
        channel = before.channel
        voice = discord.VoiceClient(client,channel).guild.voice_client 
        
        if after.channel != None:
            
            await voice.disconnect(force=True)
            await after.channel.connect(self_deaf= True)
        elif after.channel == None:
            server = member.guild
            arquivo = (f'audios/{server}.mp3')

            await voice.disconnect(force=True)
            
            lpessoas.remove(member.name)
            print(lpessoas)
            if os.path.exists(arquivo):
                os.remove(arquivo)
    #elif member == client.user and after.channel == None:
        #channel = before.channel
        #voice = discord.VoiceClient(client,channel).guild.voice_client
        
        #await voice.disconnect(force=True)
        #for pessoa in before.channel.members:
            
            #if pessoa.name in lpessoas:
            #    lpessoas.remove(pessoa.name)
            #    print(lpessoas)

    #!!!LEMBRAR DE ARRUMAR!!!
    #ISSO QUEBRA O MOMENTO EM QUE O BOT SEGUE O MEMBRO PARA A CALL QUE ELE FOR
    #!!!LEMBRAR DE ARRUMAR!!!
client.run(token)
