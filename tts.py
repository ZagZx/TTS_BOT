#METAS: 1° comando para definir um canal para o bot | 
#       2° fazer o bot só falar as mensagens de quem digitou zentrar

import discord
from gtts import gTTS
import os
from tok import token

idioma = 'pt'

intents = discord.Intents.all()

client = discord.Client(intents=intents)

comandos = ['zentrar','zair','zparar']

@client.event
async def on_ready():
    print(f'Estou online com o nome de {client.user}')



@client.event

async def on_message(message):
    global comandos
    
    if message.author != client.user:
        
            chanel = client.get_channel(message.author.voice.channel.id)
            voice = discord.VoiceClient(client,chanel).guild.voice_client
            arquivo = (f'{discord.VoiceClient(client,chanel).guild}.mp3')
            
            if message.content.startswith('zentrar'):
                await chanel.connect(self_deaf=True)
                await message.channel.send(f'Entrei em {chanel}')
                
                
                
            if  voice in client.voice_clients and message.content.startswith('zair'):
                voice = discord.VoiceClient(client,chanel).guild.voice_client
                await voice.disconnect(force=True)
                await message.channel.send('Tá bom já tô indo :C')
                if os.path.exists(f"servidores/{arquivo}"):
                    os.remove(f"servidores/{arquivo}")
            
            if voice in client.voice_clients and message.content.startswith('zparar'):
                voice.stop()

            if voice in client.voice_clients and not any(message.content == comandos[a] for a in range(0,len(comandos))):  
                gTTS(text=message.content,lang=idioma,slow=True).save(f"servidores/{arquivo}")
                source = discord.FFmpegPCMAudio(source= f'servidores/{arquivo}')
                voice.play(source)
@client.event

async def on_voice_state_update(member, before, after):
    if before.channel and member != client.user:
        channel = before.channel
        voice = discord.VoiceClient(client,channel).guild.voice_client
        server = member.guild
        arquivo = (f'{server}.mp3')
        if voice in client.voice_clients and len(channel.members) == 1:
            await voice.disconnect(force=True)
            os.remove(f"servidores/{arquivo}")
             
client.run(token)
