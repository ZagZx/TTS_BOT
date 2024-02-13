#METAS: 1° comando para definir um canal para o bot | 2° fazer funcionar em mais de um servidor ao mesmo tempo
#       3° Esconder o token

import discord
from gtts import gTTS
from tok import token
from os import remove

idioma = 'pt'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

entrou = False



@client.event
async def on_ready():
    print(f'Estou online com o nome de {client.user}')

@client.event

async def on_message(message):
    global entrou #problema no entrou, a variável é alterada por outro servidor
    

    if message.author != client.user:
        
        if message.content.startswith('zentrar'):
            chanel = client.get_channel(message.author.voice.channel.id)
            await chanel.connect(self_deaf=True)
            await message.channel.send(f'Entrei em {chanel}')
            
            entrou = True
            print(entrou)

        if message.content.startswith('zair'):
            chanel = client.get_channel(message.author.voice.channel.id)
            voice = discord.VoiceClient(client,chanel).guild.voice_client
            await voice.disconnect(force=True)
            await message.channel.send('Tá bom já tô indo :C')
            entrou = False
            print(entrou)

        if entrou and message.content.startswith('zparar'):
            chanel = client.get_channel(message.author.voice.channel.id)
            voice = discord.VoiceClient(client,chanel).guild.voice_client
            voice.stop()

        if entrou and message.content != 'zentrar' and message.content != 'zparar':   
            chanel = client.get_channel(message.author.voice.channel.id)
            gTTS(text=message.content,lang=idioma,slow=True).save('tts.mp3')
            voice = discord.VoiceClient(client,chanel).guild.voice_client
            source = discord.FFmpegPCMAudio(source='tts.mp3')
            voice.play(source)
            #if voice.is_playing() == False: #!NÃO ESTÁ ATIVANDO!#
             #   remove('tts.mp3')
            
client.run(token)