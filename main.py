#METAS: 1° comando para definir um canal para o bot | 

import discord
from gtts import gTTS
import os
from toke import token

idioma = 'pt'

intents = discord.Intents.all()

client = discord.Client(intents=intents)

comandos = ['zentrar','zair','zparar', 'zpause']

lpessoas = []

@client.event
async def on_ready():
    print(f'Estou online com o nome de {client.user}')

@client.event
async def on_disconnect():
    global lpessoas

    if lpessoas and client.voice_clients:
        lpessoas = []
        for a in client.voice_clients:
            await a.disconnect(force=True)
@client.event

async def on_message(message: discord.Message):
    global comandos
    global lpessoas

    if message.author != client.user and not message.attachments:
            if message.author.voice != None:
                chanel = client.get_channel(message.author.voice.channel.id)
                guild = discord.VoiceClient(client,chanel).guild
                    
                voice = discord.VoiceClient(client,chanel).guild.voice_client
                arquivo = (f'audios/{guild}.mp3')
            
                try:
                    if message.content.startswith('zentrar'):
                        await chanel.connect(self_deaf=True)
                        await message.channel.send(f'Entrei em {chanel.mention}')
                        lpessoas.append(message.author.name)
                        print(lpessoas)
                except:
                    await message.channel.send(f'{message.author.mention}Já estou em uma call')
                if message.author.name in lpessoas and message.content.startswith('zair'):
                
                    await voice.disconnect(force=True)
                    await message.channel.send('Tá bom já tô indo :C')

                    lpessoas.remove(message.author.name)
                    print(lpessoas)
                    if os.path.exists(arquivo):
                        os.remove(arquivo)
                elif message.author.name not in lpessoas and message.content.startswith('zair'):
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
            if message.content.startswith('zhelp') or client.user.mentioned_in(message) and not message.mention_everyone:
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

    if before.channel != after.channel and member != client.user and member.name in lpessoas: #aqui
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
   
client.run(token)
