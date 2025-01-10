'''Módulo com as funções utilizadas para armazenar e manipular os dados'''

import discord

import os
import json

pathConfig = './dados/config.json'
pathApoio = './dados/apoiadores.json'

def FirstRun():
    '''Checa se arquivos necessários para o funcionamento do bot existem e os cria'''

    if not os.path.exists('./toke.py'):
        with open('toke.py', 'w', encoding="UTF-8") as file:
            file.write('token = "seu token aqui, não retire as aspas"')

    if not os.path.exists('./audios'):
        os.mkdir('./audios')

    if not os.path.exists('./dados'):
        os.mkdir('./dados')    

    if not os.path.exists(pathApoio):
        with open(pathApoio, 'w') as file:
            file.write('{\n}')
    
    if not os.path.exists(pathConfig):
        with open(pathConfig, 'w') as file:
            file.write('{\n}')


def DefaultConfigs(client: discord.Client):
    '''Checa se todos os servidores que o bot está, tem uma configuração no banco de dados, se algum
    não tiver, então coloca as configurações padrão.
    
    - Configurações padrão: 
        - chats de mensagem: todos 
        - idioma da voz: pt_br

    '''

    with open('config.json', 'r') as fileread:
            dados = json.load(fileread)

    for server in client.guilds: 
        if str(server.id) not in dados.keys():
            dados.update({server.id:"todos"})
            with open('config.json','w') as fileWrite:
                json.dump(dados,fileWrite, indent=4)